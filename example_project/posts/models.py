from django.db import models
from django.core.urlresolvers import reverse

from embed_video.fields import EmbedVideoField


class Post(models.Model):
    title = models.CharField(max_length=50)
    video = EmbedVideoField(
        verbose_name='My media link',
        help_text='Link to a YouTube, Soundcloud or Vimeo clip.'
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
