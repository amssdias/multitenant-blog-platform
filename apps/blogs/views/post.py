from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from apps.blogs.forms.post_form import PostForm
from apps.blogs.models import Post
from apps.blogs.views.mixins.post_publish import PostPublishActionMixin
from apps.site_config.models import SiteSettings
from bloggies.mixins.tenant_mixin import TenantLoginRequiredMixin


class PostDetailView(DetailView):
    model = Post
    template_name = "blogs/post_detail.html"
    context_object_name = "post"



class PostCreateView(PostPublishActionMixin, FormView, TenantLoginRequiredMixin):
    template_name = "blogs/post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("blogs:tenant_index")


class PostEditView(PostPublishActionMixin, UpdateView, TenantLoginRequiredMixin):
    template_name = "blogs/post_form.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("blogs:tenant_index")


class PostDeleteView(DeleteView, TenantLoginRequiredMixin):
    model = Post
    template_name = "blogs/post_confirm_delete.html"
    success_url = reverse_lazy("blogs:tenant_index")

    def get_context_data(self, **kwargs):
        """Check for auth token and provide user data in template context."""
        context = super().get_context_data(**kwargs)
        return context
