from django.test import TestCase, Client
from django.urls import reverse

class SetCSRFCookieViewTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_set_csrf_cookie(self):
		response = self.client.get(reverse('csrf-setter:set_csrf_cookie'), secure=True)
		self.assertEqual(response.status_code, 204)
		self.assertIn('csrftoken', response.cookies)