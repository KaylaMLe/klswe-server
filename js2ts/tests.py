from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')

    def test_create_user(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.email, 'test@example.com')

    def test_login_user(self):
        response = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)