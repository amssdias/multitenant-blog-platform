from django.http import HttpResponseRedirect

from apps.blogs.constants import POST_ACTION_PUBLISH, POST_ACTION_DRAFT


class PostPublishActionMixin:
    """
    Adds publish/draft action constants to the template context
    and sets `is_published` based on the pressed submit button.
    """

    action_field_name = "action"
    publish_action = POST_ACTION_PUBLISH
    draft_action = POST_ACTION_DRAFT

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["POST_ACTION_PUBLISH"] = self.publish_action
        ctx["POST_ACTION_DRAFT"] = self.draft_action
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)

        action = self.request.POST.get(self.action_field_name)
        obj.is_published = (action == self.publish_action)

        obj.save()
        form.save_m2m()  # safe; only matters if form has M2M
        self.object = obj  # important for CreateView/UpdateView internals

        return HttpResponseRedirect(self.get_success_url())
