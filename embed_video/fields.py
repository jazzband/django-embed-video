from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from .base import detect_backend, NoIdFound, UnknownBackendException

__all__ = ('EmbedVideoField', 'EmbedVideoFormField')


class EmbedVideoField(models.URLField):
    def formfield(self, **kwargs):
        defaults = {'form_class': EmbedVideoFormField}
        defaults.update(kwargs)
        return super(EmbedVideoField, self).formfield(**defaults)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        cls_name = '%s.%s' % (
            self.__class__.__module__,
            self.__class__.__name__
        )
        args, kwargs = introspector(self)
        return (cls_name, args, kwargs)


class EmbedVideoFormField(forms.URLField):
    def validate(self, url):
        super(EmbedVideoFormField, self).validate(url)
        try:
            detect_backend(url)
        except UnknownBackendException:
            raise forms.ValidationError(_(u'URL could not be recognized.'))
        except NoIdFound:
            raise forms.ValidationError(_(u'Video Id not found .'))

        return url
