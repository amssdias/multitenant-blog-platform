from django import forms

from apps.blogs.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={
                "class": "form-control w-100",
                "placeholder": "Write your content here",
                "style": "height: 300px",
                "wrap": "soft",
            }),
        }
