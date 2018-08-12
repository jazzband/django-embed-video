from django import forms, VERSION
from django.utils.safestring import mark_safe

from .backends import detect_backend, UnknownBackendException, \
    VideoDoesntExistException
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
        """
        :type attrs: dict
        """
        default_attrs = {'size': '40'}

        if attrs:
            default_attrs.update(attrs)

        super(AdminVideoWidget, self).__init__(default_attrs)

    def render(self, name, value='', attrs=None, size=(420, 315), renderer=None):
        """
        :type name: str
        :type attrs: dict
        """

        if VERSION < (1, 11):
            # The renderer argument was added in 1.11.
            # https://docs.djangoproject.com/en/1.11/ref/forms/widgets/#django.forms.Widget.render
            output = super(AdminVideoWidget, self).render(name, value, attrs)
        else:
            # Support for Widget.render() methods without the renderer argument is removed in 2.1
            output = super(AdminVideoWidget, self).render(name, value, attrs, renderer)

        if not value:
            return output

        try:
            backend = detect_backend(value)
            return mark_safe(self.output_format.format(
                video=backend.get_embed_code(*size),
                input=output,
            ))
        except (UnknownBackendException, VideoDoesntExistException):
            return output


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
        """
        :type db_field: str
        """
        if isinstance(db_field, EmbedVideoField):
            return db_field.formfield(widget=AdminVideoWidget)

        return super(AdminVideoMixin, self)\
            .formfield_for_dbfield(db_field, **kwargs)
