from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class ReceivePdfTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.url = reverse("pdf-to-form:receive_pdf")

	def test_receive_pdf_with_valid_pdf(self):
		# Create a simple PDF file
		pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n278\n%%EOF"
		uploaded_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

		response = self.client.post(self.url, {"pdf": uploaded_file}, secure=True)

		self.assertEqual(response.status_code, 200)  # Adjust the expected status code as needed

	def test_receive_pdf_with_invalid_file_type(self):
		# Create a non-PDF file
		non_pdf_content = b"This is not a PDF file."
		uploaded_file = SimpleUploadedFile("test.txt", non_pdf_content, content_type="text/plain")

		response = self.client.post(self.url, {"pdf": uploaded_file}, secure=True)

		self.assertEqual(response.status_code, 400)
		self.assertIn("Expected a PDF file but got a different file type.", response.content.decode())

	def test_receive_pdf_with_no_file(self):
		response = self.client.post(self.url, {}, secure=True)

		self.assertEqual(response.status_code, 400)
		self.assertIn("Either no file uploaded or incorrect form field name", response.content.decode())