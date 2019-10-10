from django.conf.urls import url

from .views import PostListView, PostDetailView

urlpatterns = [
    url(r"(?P<pk>\d+)/$", PostDetailView.as_view(), name="detail"),
    url(r"$", PostListView.as_view(), name="list"),
]
