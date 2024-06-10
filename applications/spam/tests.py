from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from applications.spam.models import Contact

User = get_user_model()


class ContactAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_contact(self):
        url = reverse("contact-list")
        data = {
            "email": "johndoe@example.com",  # Убедитесь, что значение email соответствует "johndoe@example.com"
            "message": "Hello, this is a test message."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #
    def test_delete_contact(self):
        contact = Contact.objects.create(
            email="johndoe@example.com",
        )
        url = reverse("contact-detail", args=[contact.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
