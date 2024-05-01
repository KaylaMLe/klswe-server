from django.test import TestCase
from django.urls import reverse
from .models import CodeText


class TranslateTestCase(TestCase):
	def test_insecure_request_redirect(self):
		"""Test that an insecure request is redirected to a secure request.
		
		All insecure requests to any endpoint should be redirected to a secure request. This particular
		endpoint is chosen arbitrarily.
		"""
		response = self.client.post(reverse("translate:store_code_text"))
		self.assertEqual(response.status_code, 301)

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

	def test_translate_code(self):
		"""Test that code can be translated successfully.
		
		This test checks that the translate code endpoint returns a valid response.
		"""

		test_js = """
		function add(a, b) {
			return a + b;
		}
		"""
		response = self.client.post(
			reverse("translate:translate_code"),
			{"code": test_js},
			secure=True
		)

		# tests for accuracy are handled in the gemini repo
		# this test only checks that the response is successful
		self.assertEqual(response.status_code, 200)

		translated_code = response.content.decode()
		self.assertTrue(isinstance(translated_code, str))
		self.assertNotEqual(translated_code, "")