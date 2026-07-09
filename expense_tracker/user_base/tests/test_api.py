from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user_base.models import UserBase

class AuthAPITests(APITestCase):

    def test_user_registration(self):

        data = {
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "mobile_number": "9999999999"
        }

        response = self.client.post(
            reverse("user-register"),
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            UserBase.objects.count(),
            1
        )
    def test_user_login(self):

        UserBase.objects.create_user(
            email="test@example.com",
            password="StrongPassword123!",
            mobile_number="9999999999"
        )

        response = self.client.post(
            reverse("user-login"),
            {
                "email": "test@example.com",
                "password": "StrongPassword123!"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "token",
            response.data
        )
    def test_login_invalid_credentials(self):

        UserBase.objects.create_user(
            email="test@example.com",
            password="StrongPassword123!",
            mobile_number="9999999999"
        )

        response = self.client.post(
            reverse("user-login"),
            {
                "email": "test@example.com",
                "password": "wrongpassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )