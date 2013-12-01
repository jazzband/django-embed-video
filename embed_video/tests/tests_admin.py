from unittest import TestCase

from django.forms import TextInput

from embed_video.admin import AdminVideoWidget, AdminVideoMixin
from embed_video.backends import VimeoBackend
from embed_video.fields import EmbedVideoField, EmbedVideoFormField


class AdminVideoWidgetTestCase(TestCase):
    def test_size(self):
        widget = AdminVideoWidget()
        self.assertTrue('size' in widget.attrs)

    def test_overwrite_size(self):
        widget = AdminVideoWidget(attrs={'size': 0})
        self.assertEqual(widget.attrs['size'], 0)

    def test_add_to_attrs(self):
        widget = AdminVideoWidget(attrs={'name': 'foo'})
        self.assertEqual(widget.attrs['name'], 'foo')
        self.assertTrue('size' in widget.attrs)

    def test_render_empty_value(self):
        widget = AdminVideoWidget(attrs={'size': '0'})
        self.assertEqual(widget.render('foo'),
                         '<input name="foo" size="0" type="text" />')

    def test_render(self):
        backend = VimeoBackend('https://vimeo.com/1')
        widget = AdminVideoWidget(attrs={'size': '0'})
        widget.output_format = '{video}{input}'

        self.assertEqual(
            widget.render('foo', backend.url, size=(100, 100)),
            '<input name="foo" size="0" type="text" value="%s" />'
                % backend.url
        )

    def test_get_embed_code(self):
        backend = VimeoBackend('https://vimeo.com/1')
        widget = AdminVideoWidget(attrs={'size': '0'})
        widget.output_format = '{video}{input}'

        self.assertEqual(
            backend.get_embed_code(100, 100),
            '<iframe width="100" height="100" src="%s" frameborder="0" allowfullscreen></iframe>'
                % backend.url
        )
    def test_incorrect_value(self):
        widget = AdminVideoWidget()
        self.assertEqual(widget.render('foo', 'abcd'),
             '<input name="foo" size="40" type="text" value="abcd" />')


class AdminVideoMixinTestCase(TestCase):
    def test_embedvideofield(self):
        foo = EmbedVideoField()
        mixin = AdminVideoMixin()
        self.assertTrue(isinstance(mixin.formfield_for_dbfield(foo),
                                   EmbedVideoFormField))

    def test_other_fields(self):
        class Parent(object):
            def formfield_for_dbfield(*args, **kwargs):
                raise Exception

        class MyAdmin(AdminVideoMixin, Parent):
            pass

        myadmin = MyAdmin()
        self.assertRaises(Exception, myadmin.formfield_for_dbfield, 'foo')
