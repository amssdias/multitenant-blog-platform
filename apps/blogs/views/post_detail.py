from django.views.generic.detail import DetailView

from apps.blogs.models import Post


class PostDetailView(DetailView):
    model = Post
    template_name = "blogs/post_detail.html"
    context_object_name = "post"
