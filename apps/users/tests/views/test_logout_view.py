from django.test import override_settings, RequestFactory
from django.urls import reverse
from django.db import connection
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from apps.users.tests.factories.users import UserFactory
from apps.users.views.logout import LogoutCustomView


class TestLogoutCustomView(TenantTestCase):
    """
    Uses django-tenants TenantTestCase so tenant schema + domain exist.
    Uses TenantClient so middleware sets request.tenant based on HTTP_HOST.
    """

    @classmethod
    def setup_tenant(cls, tenant):
        owner = UserFactory(
            username="test1",
            email="test1@example.com",
        )
        tenant.owner = owner
        tenant.name = "Test Tenant"
        tenant.schema_name = "testtenant1"
        tenant.save()

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.client = TenantClient(self.tenant)
        self.logout_url = reverse("users:logout")

    def tearDown(self):
        connection.set_schema_to_public()
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        connection.set_schema_to_public()
        super().tearDownClass()

    @override_settings(DEBUG=True)
    def test_logout_redirects_to_http_with_port_when_debug_true(self):
        response = self.client.post(self.logout_url, follow=False, HTTP_HOST=self.domain.domain)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(response["Location"], f"http://{self.domain.domain}:80/")

    @override_settings(DEBUG=False)
    def test_logout_redirects_to_https_with_port_when_debug_false(self):
        response = self.client.post(self.logout_url, follow=False)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(response["Location"], f"https://{self.domain.domain}:80/")

    def test_logout_location_ends_with_trailing_slash(self):
        response = self.client.post(self.logout_url, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].endswith("/"))

    @override_settings(DEBUG=True)
    def test_get_success_url_uses_request_port(self):
        request = self.factory.post("/", SERVER_PORT="1234", HTTP_HOST=self.domain.domain)
        request.tenant = self.tenant

        view = LogoutCustomView()
        view.request = request

        self.assertEqual(view.get_success_url(), f"http://{self.domain.domain}:1234/")

    @override_settings(DEBUG=False)
    def test_get_success_url_returns_https_when_debug_false(self):
        request = self.factory.post("/", SERVER_PORT="9999", HTTP_HOST=self.domain.domain)
        request.tenant = self.tenant

        view = LogoutCustomView()
        view.request = request

        self.assertEqual(view.get_success_url(), f"https://{self.domain.domain}:9999/")
