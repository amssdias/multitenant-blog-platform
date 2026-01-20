from django.urls import reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from apps.blogs.constants import POST_ACTION_PUBLISH, POST_ACTION_DRAFT
from apps.blogs.models import Post
from apps.users.tests.factories.users import UserFactory


class TestPostCreateView(TenantTestCase):

    @classmethod
    def setup_tenant(cls, tenant):
        cls.owner = UserFactory(
            username="test-post-create",
            email="test1@example.com",
        )
        tenant.owner = cls.owner
        tenant.name = "Test Tenant"
        tenant.schema_name = "test-post-create"
        tenant.save()

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        self.create_url = reverse("blogs:create-post")

    def tenant_force_login(self, user=None):
        user = user or self.owner
        self.client.force_login(user)

        session = self.client.session
        session["auth_tenant_id"] = str(self.tenant.id)
        session.save()

    def test_post_create_requires_login(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

    def test_post_create_context_has_action_constants(self):
        self.tenant_force_login()
        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["POST_ACTION_PUBLISH"], POST_ACTION_PUBLISH)
        self.assertEqual(response.context["POST_ACTION_DRAFT"], POST_ACTION_DRAFT)

    def test_post_create_publish_sets_is_published_true(self):
        self.tenant_force_login()

        payload = {
            "title": "My post",
            "content": "<p>content</p>",
            "action": POST_ACTION_PUBLISH,
        }

        response = self.client.post(self.create_url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("blogs:tenant_index"))

        post = Post.objects.get(title="My post")
        self.assertTrue(post.is_published)

    def test_post_create_draft_sets_is_published_false(self):
        self.tenant_force_login()

        payload = {
            "title": "Draft post",
            "content": "<p>draft</p>",
            "action": POST_ACTION_DRAFT,
        }

        response = self.client.post(self.create_url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("blogs:tenant_index"))

        post = Post.objects.get(title="Draft post")
        self.assertFalse(post.is_published)
