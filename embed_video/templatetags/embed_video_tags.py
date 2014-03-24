from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe
import re
import logging
import requests

from ..backends import detect_backend, VideoBackend, \
    VideoDoesntExistException, UnknownBackendException

register = Library()

logger = logging.getLogger(__name__)


@register.tag('video')
class VideoNode(Node):
    """
    Template tag ``video``. It gives access to all
    :py:class:`~embed_video.backends.VideoBackend` variables.

    Usage (shortcut):

    .. code-block:: html+django

        {% video URL [SIZE] %}

    Or as a block:

    .. code-block:: html+django

        {% video URL as VAR %}
            ...
        {% endvideo %}

    Example:

    .. code-block:: html+django

        {% video item.video "large" %}
        {% video item.video "340x200" %}
        {% video item.video "100% x 300" %}

        {% video item.video as my_video %}
            URL: {{ my_video.url }}
            Thumbnail: {{ my_video.thumbnail }}
            Backend: {{ my_video.backend }}
        {% endvideo %}

    """
    error_msg = 'Syntax error. Expected: ``{% video URL ... %}``'
    default_size = 'small'

    re_size = re.compile('(?P<width>\d+%?) *x *(?P<height>\d+%?)')

    def __init__(self, parser, token):
        self.size = None
        self.bits = token.split_contents()

        try:
            self.url = parser.compile_filter(self.bits[1])
        except IndexError:
            raise TemplateSyntaxError(self.error_msg)

        if self.bits[-2] == 'as':
            self.nodelist_file = parser.parse(('endvideo',))
            parser.delete_first_token()
        else:
            try:
                self.size = parser.compile_filter(self.bits[2])
            except IndexError:
                self.size = self.default_size

    def render(self, context):
        url = self.url.resolve(context)

        try:
            if self.size:
                return self.__render_embed(url, context)
            else:
                return self.__render_block(url, context)
        except requests.Timeout:
            logger.exception('Timeout reached during rendering embed video (`{0}`)'.format(url))
        except UnknownBackendException:
            logger.exception('Backend wasn\'t recognised (`{0}`)'.format(url))
        except VideoDoesntExistException:
            logger.exception('Attempt to render not existing video (`{0}`)'.format(url))

        return ''

    def __render_embed(self, url, context):
        size = self.size.resolve(context) \
            if hasattr(self.size, 'resolve') else self.size
        return self.embed(url, size, context=context)

    def __render_block(self, url, context):
        as_var = self.bits[-1]

        context.push()
        context[as_var] = self.get_backend(url, context=context)
        output = self.nodelist_file.render(context)
        context.pop()

        return output

    @staticmethod
    def get_backend(backend_or_url, context=None):
        """
        Returns instance of VideoBackend. If context is passed to the method
        and request is secure, than the is_secure mark is set to backend.
        
        A string or VideoBackend instance can be passed to the method.
        """
        
        backend = backend_or_url if isinstance(backend_or_url, VideoBackend) \
                    else detect_backend(backend_or_url)
                    
        if context and 'request' in context:
            backend.is_secure = context['request'].is_secure()

        return backend

    @staticmethod
    def embed(url, size, context=None):
        """
        Direct render of embed video.
        """
        backend = VideoNode.get_backend(url, context=context)
        width, height = VideoNode.get_size(size)
        return mark_safe(backend.get_embed_code(width=width, height=height))

    @staticmethod
    def get_size(value):
        """
        Predefined sizes:

        ======== ======== =========
        size     width    height
        ======== ======== =========
        tiny     420      315
        small    480      360
        medium   640      480
        large    960      720
        huge     1280     960
        ======== ======== =========

        You can also use custom size - in format ``WIDTHxHEIGHT``
        (eg. ``500x400``).
        """
        sizes = {
            'tiny': (420, 315),
            'small': (480, 360),
            'medium': (640, 480),
            'large': (960, 720),
            'huge': (1280, 960),
        }

        if value in sizes:
            return sizes[value]

        try:
            size = VideoNode.re_size.match(value)
            return [size.group('width'), size.group('height')]
        except AttributeError:
            raise TemplateSyntaxError(
                'Incorrect size.\nPossible format is WIDTHxHEIGHT or using '
                'predefined size ({sizes}).'.format(sizes=', '.join(sizes.keys()))
            )

    def __iter__(self):
        for node in self.nodelist_file:
            yield node

    def __repr__(self):
        return '<VideoNode "%s">' % self.url


@register.filter(is_safe=True)
def embed(backend, size='small'):
    """
    .. warning::
        .. deprecated:: 0.7
            Use :py:func:`VideoNode.embed` instead.

    Same like :py:func:`VideoNode.embed` tag but **always uses insecure
    HTTP protocol**.

    Usage:

    .. code-block:: html+django

        {{ URL|embed:SIZE }}

    Example:

    .. code-block:: html+django

        {{ 'http://www.youtube.com/watch?v=guXyvo2FfLs'|embed:'large' }}
    """
    return VideoNode.embed(backend, size)
