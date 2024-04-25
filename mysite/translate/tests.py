from django.test import TestCase
from django.urls import reverse
from .models import CodeText


class TranslateTestCase(TestCase):
	def test_store_get_code_text(self):
		"""Test that a CodeText object can be stored, retrieved, and deleted.
		
		This test first sends a POST request to store a new CodeText object, then sends a GET request
		to retrieve it, and finally sends a DELETE request to delete it. It checks that the responses
		are successful and that the retrieved and deleted CodeText objects have the correct code.
		"""
		# stores code text
		response = self.client.post(
			reverse("translate:store_code_text"),
			{"code": "Test code"},
			secure=True
		)
		self.assertEqual(response.status_code, 200)

		# retrieves code text and checks that the code is identical to the stored code
		code_text = CodeText.objects.get(code="Test code")
		response = self.client.get(
			reverse("translate:get_code_text", args=[code_text.pk]),
			secure=True
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn("Test code", response.content.decode())

		# deletes code text and checks that it no longer exists
		response = self.client.delete(
			reverse("translate:delete_code_text", args=[code_text.pk]),
			secure=True
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(CodeText.objects.filter(code="Test code").exists())
