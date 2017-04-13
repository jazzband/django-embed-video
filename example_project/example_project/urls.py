from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns() \
    + [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('posts.urls', namespace='posts')),
    ]
