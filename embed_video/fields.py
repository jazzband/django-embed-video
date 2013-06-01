from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from .base import detect_backend

__all__ = ('EmbedVideoField', 'EmbedVideoFormField')


class EmbedVideoField(models.URLField):
    def formfield(self, **kwargs):
        defaults = {'form_class': EmbedVideoFormField}
        defaults.update(kwargs)
        return super(EmbedVideoField, self).formfield(**defaults)


class EmbedVideoFormField(forms.URLField):
    def validate(self, url):
        super(EmbedVideoFormField, self).validate(url)

        try:
            detect_backend(url)
        except:
            raise forms.ValidationError(_(u'URL could not be recognized.'))

        return url
