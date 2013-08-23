from django.conf.urls import patterns, url

from .views import PostListView, PostDetailView

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
    url(r'$', PostListView.as_view(), name='list'),
)
