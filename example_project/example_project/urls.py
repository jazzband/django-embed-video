from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from django.contrib import admin

admin.autodiscover()

urlpatterns = staticfiles_urlpatterns() + [
    path("admin/", admin.site.urls),
    path("", include(("posts.urls", "posts"))),
]
