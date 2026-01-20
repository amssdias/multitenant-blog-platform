from django.urls import reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django_tenants.utils import schema_context

from apps.blogs.constants import POST_ACTION_PUBLISH, POST_ACTION_DRAFT
from apps.blogs.tests.factories.post import PostFactory
from apps.users.tests.factories.users import UserFactory


class TestPostEditView(TenantTestCase):

    @classmethod
    def setup_tenant(cls, tenant):
        cls.owner = UserFactory(
            username="test-post-edit",
            email="test1@example.com",
        )
        tenant.owner = cls.owner
        tenant.name = "Test Tenant"
        tenant.schema_name = "test-post-edit"
        tenant.save()

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)

    def tenant_force_login(self, user=None):
        user = user or self.owner
        self.client.force_login(user)

        session = self.client.session
        session["auth_tenant_id"] = str(self.tenant.id)
        session.save()

    def test_post_edit_requires_login(self):
        with schema_context(self.tenant.schema_name):
            post = PostFactory()

        edit_url = reverse("blogs:post_edit", args=[post.id])

        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 302)

    def test_post_edit_context_has_action_constants(self):
        self.tenant_force_login()
        post = PostFactory()
        edit_url = reverse("blogs:post_edit", args=[post.id])

        response = self.client.get(edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["POST_ACTION_PUBLISH"], POST_ACTION_PUBLISH)
        self.assertEqual(response.context["POST_ACTION_DRAFT"], POST_ACTION_DRAFT)

    def test_post_edit_publish_sets_is_published_true(self):
        self.tenant_force_login()

        post = PostFactory(title="Old", is_published=False)
        edit_url = reverse("blogs:post_edit", args=[post.id])

        payload = {
            "title": "Old",
            "content": "Updated body",
            "action": POST_ACTION_PUBLISH,
        }

        response = self.client.post(edit_url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("blogs:tenant_index"))

        post.refresh_from_db()
        self.assertTrue(post.is_published)
        self.assertEqual(post.content, "Updated body")

    def test_post_edit_draft_sets_is_published_false(self):
        self.tenant_force_login()

        post = PostFactory(title="Pub", content="Body", is_published=True)
        edit_url = reverse("blogs:post_edit", args=[post.id])

        payload = {
            "title": "Pub",
            "content": "Body changed",
            "action": POST_ACTION_DRAFT,
        }

        response = self.client.post(edit_url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("blogs:tenant_index"))

        post.refresh_from_db()
        self.assertFalse(post.is_published)
        self.assertEqual(post.content, "Body changed")
