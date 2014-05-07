import re
import logging
import requests
from collections import defaultdict

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str

from ..backends import detect_backend, VideoBackend, \
    VideoDoesntExistException, UnknownBackendException

register = Library()

logger = logging.getLogger(__name__)

# Used for parsing keyword arguments passed in as key-value pairs
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


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
    error_msg = 'Syntax error. Expected: ``{% video URL ' \
                '[size] [key1=val1 key2=val2 ...] [as var] %}``'
    default_size = 'small'

    re_size = re.compile('(?P<width>\d+%?) *x *(?P<height>\d+%?)')

    def __init__(self, parser, token):
        self.size = None
        self.bits = token.split_contents()
        self.query = None

        try:
            self.url = parser.compile_filter(self.bits[1])
        except IndexError:
            raise TemplateSyntaxError(self.error_msg)

        # Determine if the tag is being used as a context variable
        if self.bits[-2] == 'as':
            option_bits = self.bits[2:-2]
            self.nodelist_file = parser.parse(('endvideo',))
            parser.delete_first_token()
        else:
            option_bits = self.bits[2:]

            # Size must be the first argument and is only accepted when this is
            # used as a template tag (but not when used as a block tag)
            if len(option_bits) != 0 and '=' not in option_bits[0]:
                self.size = parser.compile_filter(option_bits[0])
                option_bits = option_bits[1:]
            else:
                self.size = self.default_size

        # Parse arguments passed in as KEY=VALUE pairs that will be added to
        # the URL as a GET query string
        if len(option_bits) != 0:
            self.query = defaultdict(list)

        for bit in option_bits:
            match = kw_pat.match(bit)
            key = smart_str(match.group('key'))
            value = Variable(smart_str(match.group('value')))
            self.query[key].append(value)

    def render(self, context):
        # Attempt to resolve any parameters passed in.
        if self.query is not None:
            resolved_query = defaultdict(list)
            for key, values in self.query.items():
                for value in values:
                    resolved_value = value.resolve(context)
                    resolved_query[key].append(resolved_value)
        else:
            resolved_query = None

        url = self.url.resolve(context)
        try:
            if self.size:
                return self.__render_embed(url, context, resolved_query)
            else:
                return self.__render_block(url, context, resolved_query)
        except requests.Timeout:
            logger.exception('Timeout reached during rendering embed video (`{0}`)'.format(url))
        except UnknownBackendException:
            logger.exception('Backend wasn\'t recognised (`{0}`)'.format(url))
        except VideoDoesntExistException:
            logger.exception('Attempt to render not existing video (`{0}`)'.format(url))

        return ''

    def __render_embed(self, url, context, query):
        size = self.size.resolve(context) \
            if hasattr(self.size, 'resolve') else self.size
        return self.embed(url, size, context=context, query=query)

    def __render_block(self, url, context, query):
        as_var = self.bits[-1]

        context.push()
        context[as_var] = self.get_backend(url, context=context, query=query)
        output = self.nodelist_file.render(context)
        context.pop()

        return output

    @staticmethod
    def get_backend(backend_or_url, context=None, query=None):
        """
        Returns instance of VideoBackend. If context is passed to the method
        and request is secure, than the is_secure mark is set to backend.

        A string or VideoBackend instance can be passed to the method.
        """

        backend = backend_or_url if isinstance(backend_or_url, VideoBackend) \
            else detect_backend(str(backend_or_url))

        if context and 'request' in context:
            backend.is_secure = context['request'].is_secure()

        backend.update_query(query)

        return backend

    @staticmethod
    def embed(url, size, GET=None, context=None, query=None):
        """
        Direct render of embed video.
        """
        backend = VideoNode.get_backend(url, context=context, query=query)
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
