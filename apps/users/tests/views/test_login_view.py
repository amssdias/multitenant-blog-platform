from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.tenants.models import Tenant, Domain
from apps.users.tests.factories.users import UserFactory

User = get_user_model()


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class TestCustomLoginView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("users:login")

        # Create tenant + domain
        cls.password = "1234"
        cls.user = UserFactory(
            username="test",
            email="test@example.com",
            password=cls.password
        )
        cls.tenant = Tenant.objects.create(name="Tenant 1", schema_name="tenant1", owner=cls.user)
        cls.domain = Domain.objects.create(
            tenant=cls.tenant,
            domain="tenant1.testserver.com",
            is_primary=True,
        )

    def setUp(self):
        Tenant.auto_create_schema = False  # 🚫 no CREATE SCHEMA, no tenant migrations

    @classmethod
    def tearDownClass(cls):
        Tenant.auto_create_schema = True
        super().tearDownClass()

    # -------------------------
    # Helpers
    # -------------------------
    def _login_payload(self, **overrides):
        payload = {
            "username": self.user.username,
            "password": self.password,
        }
        payload.update(overrides)
        return payload

    def _post_login(self, payload=None):
        payload = payload or self._login_payload()
        return self.client.post(self.url, data=payload, follow=False)

    def test_get_login_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    @override_settings(DEBUG=True)
    def test_success_login_redirects_to_http_subdomain_with_port_when_debug_true(self):
        response = self._post_login()
        self.assertEqual(response.status_code, 302)

        # get_success_url uses request.get_port() and tenant's first domain
        # Domain is "tenant1.testserver.com", port in tests is typically 80 unless you pass SERVER_PORT.
        self.assertTrue(response["Location"].startswith("http://tenant1.testserver"))

    @override_settings(DEBUG=False)
    def test_success_login_redirects_to_https_subdomain_without_port_when_debug_false(self):
        response = self._post_login()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://tenant1.testserver.com")

    def test_success_login_sets_auth_tenant_id_in_session(self):
        response = self._post_login()
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        self.assertIn("auth_tenant_id", session)
        self.assertEqual(session["auth_tenant_id"], self.tenant.id)

    def test_invalid_credentials_do_not_login_and_do_not_set_session(self):
        response = self._post_login(payload=self._login_payload(password="WrongPass123!"))

        self.assertEqual(response.status_code, 200)

        session = self.client.session
        self.assertNotIn("auth_tenant_id", session)

    def test_inactive_user_cannot_login_and_does_not_set_session(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self._post_login()
        self.assertEqual(response.status_code, 200)

        session = self.client.session
        self.assertNotIn("auth_tenant_id", session)

    @override_settings(DEBUG=False)
    def test_next_parameter_is_ignored_by_custom_get_success_url(self):
        response = self.client.post(
            f"{self.url}?next=/should-not-go-here/",
            data=self._login_payload(),
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://tenant1.testserver.com")

    def test_form_valid_sets_session_auth_tenant_id_after_login(self):
        response = self._post_login()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["auth_tenant_id"], self.tenant.id)

    def test_login_fails_if_user_has_no_tenant(self):
        UserFactory(username="u1", password="1234", is_active=True)

        response = self.client.post(self.url, data={"username": "u1", "password": "1234"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "isn’t linked to a workspace", status_code=200)

    def test_login_fails_if_tenant_has_no_domain(self):
        user = UserFactory(username="u2", password="1234", is_active=True)
        Tenant.objects.create(name="T2", schema_name="t2", owner=user)

        response = self.client.post(self.url, data={"username": "u2", "password": "1234"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "missing domain", status_code=200)
