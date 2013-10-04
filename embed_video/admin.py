from django import forms
from django.utils.safestring import mark_safe

from .backends import detect_backend
from .fields import EmbedVideoField


class AdminVideoWidget(forms.TextInput):
    """
    Widget for video input in administration. If empty it works just like
    :py:class:`django.forms.TextInput`. Otherwise it renders embedded video
    together with input field.

    .. todo::

        Django 1.6 provides better parent for this widget -
        :py:class:`django.forms.URLInput`.

    """

    output_format = u'<div style="float:left" class="video">' \
                    u'{video}<br />{input}</div>' \
                    u'<hr style="visibility: hidden; clear:both">'

    def __init__(self, attrs=None):
        default_attrs = {'size': '40'}

        if attrs:
            default_attrs.update(attrs)

        super(AdminVideoWidget, self).__init__(default_attrs)

    def render(self, name, value='', attrs=None, size=(420, 315)):
        output = super(AdminVideoWidget, self).render(name, value, attrs)

        if value:
            try:
                backend = detect_backend(value)
            except:
                pass
            else:
                output = self.output_format.format(
                    video=backend.get_embed_code(*size),
                    input=output,
                )

        return mark_safe(output)


class AdminVideoMixin(object):
    """
    Mixin using :py:class:`AdminVideoWidget` for fields with
    :py:class:`~embed_video.fields.EmbedVideoField`.

    Usage::

        from django.contrib import admin
        from embed_video.admin import AdminVideoMixin
        from .models import MyModel

        class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
            pass

        admin.site.register(MyModel, MyModelAdmin)

    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, EmbedVideoField):
            return db_field.formfield(widget=AdminVideoWidget)

        return super(AdminVideoMixin, self) \
                .formfield_for_dbfield(db_field, **kwargs)
