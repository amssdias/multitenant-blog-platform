from django import forms
from django_summernote.widgets import SummernoteWidget

from apps.blogs.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your post title"}),
            "content": SummernoteWidget(),
        }
