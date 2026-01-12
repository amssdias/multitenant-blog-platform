from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.tenants.models import Tenant, Domain

User = get_user_model()


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class TestRegisterView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("users:signup")
        cls.login_url = reverse("users:login")

    def setUp(self):
        self.valid_payload = {
            "username": "test",
            "email": "test@example.com",
            "password1": "StrongPass12345!",
            "password2": "StrongPass12345!",
            "subdomain": "test",
        }
        Tenant.auto_create_schema = False  # 🚫 no CREATE SCHEMA, no tenant migrations

    @classmethod
    def tearDownClass(cls):
        Tenant.auto_create_schema = True
        super().tearDownClass()

    def _post(self, payload):
        return self.client.post(self.url, data=payload, follow=False)

    def _assert_nothing_created(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Tenant.objects.count(), 0)
        self.assertEqual(Domain.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def _get_created_domain(self):
        """
        Adjust lookups if your Domain model differs.
        Common patterns:
          - Domain(domain="sub.example.com", tenant=tenant)
          - Domain(subdomain="sub", domain="example.com")
        """
        # Try common full-domain form first:
        full = f"{self.valid_payload['subdomain']}.testserver"
        if Domain.objects.filter(domain=full).exists():
            return Domain.objects.get(domain=full)

    def test_get_signup_page_returns_200_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_valid_post_redirects_to_login(self):
        response = self._post(self.valid_payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], self.login_url)

    def test_valid_post_creates_user_in_db(self):
        self._post(self.valid_payload)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username=self.valid_payload.get("username"))
        self.assertEqual(user.email, self.valid_payload.get("email"))

    def test_user_is_inactive_after_registration(self):
        self._post(self.valid_payload)
        user = User.objects.get(username=self.valid_payload.get("username"))

        self.assertFalse(user.is_active)

    def test_valid_post_creates_tenant_and_domain_in_db(self):
        n_tenants = Tenant.objects.count()
        n_domains = Domain.objects.count()

        self._post(self.valid_payload)

        self.assertEqual(Tenant.objects.count(), n_tenants + 1)
        self.assertGreaterEqual(Domain.objects.count(), n_domains + 1)

    def test_email_was_sent_on_successful_registration(self):
        self._post(self.valid_payload)

        self.assertGreaterEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertTrue(email.to)
        self.assertIn(self.valid_payload.get("email"), email.to)

    def test_email_contains_host_or_link_info(self):
        self._post(self.valid_payload)

        self.assertGreaterEqual(len(mail.outbox), 1)
        body = (mail.outbox[0].body or "").lower()

        self.assertIn("testserver", body)

    def test_register_without_email_is_invalid(self):
        payload = dict(self.valid_payload)
        payload["email"] = ""

        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "email", status_code=200)
        self._assert_nothing_created()

    def test_register_without_username_is_invalid(self):
        payload = dict(self.valid_payload)
        payload["username"] = ""

        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username", status_code=200)
        self._assert_nothing_created()

    def test_register_without_subdomain_is_invalid(self):
        payload = dict(self.valid_payload)
        payload["subdomain"] = ""

        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subdomain", status_code=200)
        self._assert_nothing_created()

    def test_register_without_password1_is_invalid(self):
        payload = dict(self.valid_payload)
        payload["password1"] = ""

        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "password", status_code=200)
        self._assert_nothing_created()

    def test_register_with_password_mismatch_is_invalid(self):
        payload = dict(self.valid_payload)
        payload["password2"] = "DifferentPass12345!"

        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "password", status_code=200)
        self._assert_nothing_created()
