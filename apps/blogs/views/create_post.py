from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.blogs.forms.post_form import PostForm


class PostCreateView(FormView):
    template_name = "blogs/post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("blogs:tenant_index")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Check for auth token and provide user data in template context."""
        context = super().get_context_data(**kwargs)
        request = self.request

        auth_token = request.COOKIES.get("auth_token")

        if auth_token:
            user_data = cache.get(f"auth_token:{auth_token}")

            if user_data and user_data["tenant"] == request.tenant.schema_name:
                context["user_authenticated"] = True
                context["username"] = user_data["username"]
                context["form"] = PostForm()
            else:
                context["user_authenticated"] = False

        return context
