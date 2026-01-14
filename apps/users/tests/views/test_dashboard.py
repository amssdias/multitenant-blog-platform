from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class DashboardViewTests(TestCase):
    def test_dashboard_returns_200(self):
        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_dashboard_uses_correct_template(self):
        url = reverse("dashboard")
        response = self.client.get(url)

        self.assertTemplateUsed(response, "users/dashboard.html")
