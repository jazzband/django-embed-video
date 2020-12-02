from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from embed_video.backends import (
    UnknownBackendException,
    UnknownIdException,
    VideoDoesntExistException,
    detect_backend,
)

__all__ = ("EmbedVideoField", "EmbedVideoFormField")


class EmbedVideoField(models.URLField):
    """
    Model field for embedded video. Descendant of
    :py:class:`django.db.models.URLField`.
    """

    def formfield(self, **kwargs):
        defaults = {"form_class": EmbedVideoFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class EmbedVideoFormField(forms.URLField):
    """
    Form field for embeded video. Descendant of
    :py:class:`django.forms.URLField`
    """

    def validate(self, url):
        # if empty url is not allowed throws an exception
        super().validate(url)

        if not url:
            return

        try:
            backend = detect_backend(url)
            backend.get_code()
        except UnknownBackendException:
            raise forms.ValidationError(_("URL could not be recognized."))
        except UnknownIdException:
            raise forms.ValidationError(
                _("ID of this video could not be " "recognized.")
            )
        except VideoDoesntExistException:
            raise forms.ValidationError(_("This media not found on site."))
        return url
