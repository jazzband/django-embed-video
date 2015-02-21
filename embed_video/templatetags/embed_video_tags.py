import re
import logging
import requests

from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str

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

        {% video URL [SIZE] [key1=value1, key2=value2...] %}

    Or as a block:

    .. code-block:: html+django

        {% video URL [SIZE] [key1=value1, key2=value2...] as VAR %}
            ...
        {% endvideo %}

    Examples:

    .. code-block:: html+django

        {% video item.video %}
        {% video item.video "large" %}
        {% video item.video "340x200" %}
        {% video item.video "100% x 300" query="rel=0&wmode=opaque" %}

        {% video item.video is_secure=True as my_video %}
            URL: {{ my_video.url }}
            Thumbnail: {{ my_video.thumbnail }}
            Backend: {{ my_video.backend }}
        {% endvideo %}

    """
    error_msg = 'Syntax error. Expected: ``{% video URL ' \
                '[size] [key1=val1 key2=val2 ...] [as var] %}``'
    default_size = 'small'

    re_size = re.compile('[\'"]?(?P<width>\d+%?) *x *(?P<height>\d+%?)[\'"]?')
    re_option = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')

    def __init__(self, parser, token):
        """
        :param parser: Django template parser
        :type parser: django.template.base.Parser
        :param token: Django template token
        :type token: django.template.base.Token
        """
        self.parser = parser
        self.bits = list(token.split_contents())
        self.tag_name = str(self.pop_bit())
        self.url = self.pop_bit()

        if len(self.bits) > 1 and self.bits[-2] == 'as':
            del self.bits[-2]
            self.variable_name = str(self.pop_bit(-1))
            self.nodelist_file = parser.parse(('end' + self.tag_name, ))
            parser.delete_first_token()
        else:
            self.variable_name = None

        self.size = self.pop_bit() if self.bits and '=' not in self.bits[0] else None
        self.options = self.parse_options(self.bits)

    def pop_bit(self, index=0):
        return self.parser.compile_filter(self.bits.pop(index))

    def parse_options(self, bits):
        options = {}
        for bit in bits:
            parsed_bit = self.re_option.match(bit)
            key = smart_str(parsed_bit.group('key'))
            value = self.parser.compile_filter(parsed_bit.group('value'))
            options[key] = value
        return options

    def render(self, context):
        """
        Returns generated HTML.

        :param context: Django template RequestContext
        :type context: django.template.RequestContext
        :return: Rendered HTML with embed video.
        :rtype: django.utils.safestring.SafeText | str
        """
        url = self.url.resolve(context)
        size = self.size.resolve(context) if self.size else None
        options = self.resolve_options(context)

        try:
            if not self.variable_name:
                return self.embed(url, size, context=context, **options)
            backend = self.get_backend(url, context=context, **options)
            return self.render_block(context, backend)
        except requests.Timeout:
            logger.exception('Timeout reached during rendering embed video (`{0}`)'.format(url))
        except UnknownBackendException:
            logger.exception('Backend wasn\'t recognised (`{0}`)'.format(url))
        except VideoDoesntExistException:
            logger.exception('Attempt to render not existing video (`{0}`)'.format(url))

        return ''

    def resolve_options(self, context):
        """
        :param context: Django template RequestContext
        :type context: django.template.RequestContext
        """
        options = {}
        for key in self.options:
            value = self.options[key]
            options[key] = value.resolve(context)
        return options

    def render_block(self, context, backend):
        """
        :param context: Django template RequestContext
        :type context: django.template.RequestContext
        :param backend: Given instance inherited from VideoBackend
        :type backend: VideoBackend
        :rtype: django.utils.safestring.SafeText
        """
        context.push()
        context[self.variable_name] = backend
        output = self.nodelist_file.render(context)
        context.pop()
        return output

    @staticmethod
    def get_backend(backend_or_url, context=None, **options):
        """
        Returns instance of VideoBackend. If context is passed to the method
        and request is secure, than the is_secure mark is set to backend.

        A string or VideoBackend instance can be passed to the method.

        :param backend: Given instance inherited from VideoBackend or url
        :type backend_or_url: VideoBackend | str
        :param context: Django template RequestContext
        :type context: django.template.RequestContext | None
        :rtype: VideoBackend
        """

        backend = backend_or_url if isinstance(backend_or_url, VideoBackend) \
            else detect_backend(str(backend_or_url))

        if context and 'request' in context:
            backend.is_secure = context['request'].is_secure()
        if options:
            backend.set_options(options)

        return backend

    @classmethod
    def embed(cls, url, size, context=None, **options):
        """
        Direct render of embed video.

        :param url: URL to embed video
        :type url: str
        :param size: Size of rendered block
        :type size: str
        :param context: Django template RequestContext
        :type context: django.template.RequestContext | None
        """
        backend = cls.get_backend(url, context=context, **options)
        width, height = cls.get_size(size)
        return mark_safe(backend.get_embed_code(width=width, height=height))

    @classmethod
    def get_size(cls, value):
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

        :type value: str

        :return: Returns tuple with (width, height) values.
        :rtype: tuple[int, int]
        """
        sizes = {
            'tiny': (420, 315),
            'small': (480, 360),
            'medium': (640, 480),
            'large': (960, 720),
            'huge': (1280, 960),
        }

        value = value or cls.default_size
        if value in sizes:
            return sizes[value]

        try:
            size = cls.re_size.match(value)
            return size.group('width'), size.group('height')
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
