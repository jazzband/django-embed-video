from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe, SafeText

from ..base import detect_backend, SoundCloudBackend

register = Library()


@register.tag('video')
class VideoNode(Node):
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
def embed(backend, _size='small'):
    if isinstance(backend, SafeText):
        backend = detect_backend(backend)

    size = _embed_get_size(_size)
    params = _embed_get_params(backend, size)

    return mark_safe(
        '<iframe width="%(width)d" height="%(height)d" '
        'src="%(url)s" frameborder="0" allowfullscreen>'
        '</iframe>' % params
    )


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


def _embed_get_params(backend, size):
    params = {
        'url': backend.url,
        'width': size[0],
        'height': size[1],
    }

    if isinstance(backend, SoundCloudBackend):
        params.update({'height': backend.height})

    return params


