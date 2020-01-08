from django import forms
from django.utils.safestring import mark_safe

from .backends import detect_backend, UnknownBackendException, VideoDoesntExistException
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

    output_format = (
        '<div style="float:left" class="video">'
        "{video}<br />{input}</div>"
        '<hr style="visibility: hidden; clear:both">'
    )

    def __init__(self, attrs=None):
        """
        :type attrs: dict
        """
        default_attrs = {"size": "40"}

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    def render(self, name, value="", attrs=None, size=(420, 315), renderer=None):
        """
        :type name: str
        :type attrs: dict
        """

        output = super().render(name, value, attrs, renderer)

        if not value:
            return output

        try:
            backend = detect_backend(value)
            return mark_safe(
                self.output_format.format(
                    video=backend.get_embed_code(*size), input=output
                )
            )
        except (UnknownBackendException, VideoDoesntExistException):
            return output


class AdminVideoMixin:
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

        return super().formfield_for_dbfield(db_field, **kwargs)
