from django.db import models

from bloggies.models.timestampable import Timestampable


class Post(Timestampable):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
