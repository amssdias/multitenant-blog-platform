from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from apps.blogs.forms.post_form import PostForm
from apps.blogs.models import Post
from bloggies.mixins.tenant_mixin import TenantLoginRequiredMixin
from bloggies.mixins.tenant_mixin import TenantUserContextMixin


class PostDetailView(DetailView, TenantUserContextMixin):
    model = Post
    template_name = "blogs/post_detail.html"
    context_object_name = "post"


class PostCreateView(FormView, TenantLoginRequiredMixin):
    template_name = "blogs/post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("blogs:tenant_index")

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)


class PostEditView(TenantLoginRequiredMixin, UpdateView):
    template_name = "blogs/post_form.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("blogs:tenant_index")

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)
