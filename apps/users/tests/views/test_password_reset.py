from django.test import TestCase, override_settings
from django.urls import reverse

from apps.users.tests.factories.users import UserFactory


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class PasswordResetTemplatesTests(TestCase):
    def test_password_reset_form_uses_template(self):
        url = reverse("users:password_reset")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration/password_reset_form.html")

    def test_password_reset_done_uses_template(self):
        url = reverse("users:password_reset_done")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration/password_reset_done.html")

    def test_password_reset_complete_uses_template(self):
        url = reverse("users:password_reset_complete")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration/password_reset_complete.html")


@override_settings(ROOT_URLCONF="bloggies.urls_public")
class PasswordResetFlowBehaviorTests(TestCase):
    def test_password_reset_post_redirects_to_done(self):
        user = UserFactory(
            username="dias",
            email="dias@example.com",
            password="OldPass123!",
        )

        url = reverse("users:password_reset")

        response = self.client.post(url, data={"email": user.email})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("users:password_reset_done"))
