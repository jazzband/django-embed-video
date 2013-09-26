from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from ..backends import detect_backend, VideoBackend

register = Library()


@register.tag('video')
class VideoNode(Node):
    """
    Template tag ``video``. It gives access to all
    :py:class:`~embed_video.backends.VideoBackend` variables.

    Usage:

    .. code-block:: html+django

        {% video URL as VAR %}
            ...
        {% endvideo %}

    Example:

    .. code-block:: html+django

        {% video item.video as my_video %}
            URL: {{ my_video.url }}
            Thumbnail: {{ my_video.thumbnail }}
            Backend: {{ my_video.backend }}
        {% endvideo %}

    """
    error_msg = ('Syntax error. Expected: ``video source as var``')

    def __init__(self, parser, token):
        bits = token.split_contents()

        if len(bits) < 4 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)

        self.url = parser.compile_filter(bits[1])
        self.as_var = bits[-1]

        self.nodelist_file = parser.parse(('endvideo',))
        parser.delete_first_token()

    def render(self, context):
        url = self.url.resolve(context)
        context.push()
        context[self.as_var] = detect_backend(url)
        output = self.nodelist_file.render(context)
        context.pop()
        return output

    def __iter__(self):
        for node in self.nodelist_file:
            yield node

    def __repr__(self):
        return '<VideoNode "%s">' % (self.url)


@register.filter(is_safe=True)
def embed(backend, size='small'):
    """
    Shortcut for :py:func:`VideoNode` tag.

    Usage:

    .. code-block:: html+django

        {{ URL|embed:SIZE }}

    Example:

    .. code-block:: html+django

        {{ 'http://www.youtube.com/watch?v=guXyvo2FfLs'|embed:'large' }}

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

    if not isinstance(backend, VideoBackend):
        backend = detect_backend(backend)

    _size = _embed_get_size(size)

    return mark_safe(backend.get_embed_code(width=_size[0],
                                            height=_size[1]))


def _embed_get_size(size):
    sizes = {
        'tiny': (420, 315),
        'small': (480, 360),
        'medium': (640, 480),
        'large': (960, 720),
        'huge': (1280, 960),
    }

    if size in sizes:
        return sizes[size]
    elif 'x' in size:
        return [int(x) for x in size.split('x')]

