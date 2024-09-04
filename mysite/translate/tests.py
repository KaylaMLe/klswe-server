from django.test import TestCase
from django.urls import reverse


# class TranslateTestCase(TestCase):
# 	def test_translate_code(self):
# 		"""Test that code can be translated successfully.
		
# 		This test checks that the translate code endpoint returns a valid response.
# 		"""

# 		test_js = """
# 		function add(a, b) {
# 			return a + b;
# 		}
# 		"""
# 		response = self.client.post(
# 			reverse("translate:translate_code"),
# 			{"code": test_js},
# 			content_type="application/json",
# 			secure=True
# 		)

# 		# tests for accuracy are handled in the gemini repo
# 		# this test only checks that the response is successful
# 		self.assertEqual(response.status_code, 200)

# 		translated_code = response.content.decode()
# 		self.assertTrue(isinstance(translated_code, str))
# 		self.assertNotEqual(translated_code, "")
