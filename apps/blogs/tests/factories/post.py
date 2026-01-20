import factory
from django.utils.text import slugify

from apps.blogs.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'post%d' % n)
    content = factory.Faker("text", max_nb_chars=800)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    is_published = True
