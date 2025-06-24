from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
