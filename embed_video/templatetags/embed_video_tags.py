from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from ..base import detect_backend, SoundCloundBackend

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
        return '<VideoNode>'


@register.filter(is_safe=True)
def embed(backend, _size='small'):
    sizes = {
        'tiny': (420, 315),
        'small': (480, 360),
        'medium': (640, 480),
        'large': (960, 720),
        'huge': (1280, 960),
    }

    if _size in sizes:
        size = sizes[_size]
    elif 'x' in _size:
        size = _size.split('x')

    params = {
        'url': backend.url,
        'width': int(size[0]),
        'height': int(size[1]),
    }

    if isinstance(backend, SoundCloundBackend):
        params.update({'height': backend.height})

    return mark_safe(
        '<iframe width="%(width)d" height="%(height)d" '
        'src="%(url)s" frameborder="0" allowfullscreen>'
        '</iframe>' % params
    )
