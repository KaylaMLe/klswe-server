from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import pymupdf
from os import path


class ReceivePdfTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.url = reverse("pdf-to-form:receive_pdf")
		self.snapshots_dir = path.join(path.dirname(__file__), "snapshots")

	# checks if the view can receive a PDF file and return a PDF with the expected checkbox
	def test_receive_pdf_with_valid_pdf(self):
		pdf_content = pdf_to_binary(path.join(self.snapshots_dir, "checkbox_original.pdf"))
		uploaded_file = SimpleUploadedFile(
			"checkbox_original.pdf", pdf_content, content_type="application/pdf"
		)
		response = self.client.post(
			self.url,
			{"pdf": uploaded_file, "targetChars": '[{"name": "checkbox", "char": "☐"}]'},
			secure=True
		)

		# uncomment to save new pdf snapshot
		# with open(path.join(self.snapshots_dir, "checkbox_output.pdf"), "wb") as file:
		# 	file.write(response.content)

		expected_output = pdf_to_binary(path.join(self.snapshots_dir, "checkbox_output.pdf"))
		expected_checkbox = get_annotation_rects(expected_output)
		actual_checkbox = get_annotation_rects(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(expected_checkbox, actual_checkbox)

	def test_receive_pdf_with_invalid_file_type(self):
		# Create a non-PDF file
		non_pdf_content = b"This is not a PDF file."
		uploaded_file = SimpleUploadedFile("test.txt", non_pdf_content, content_type="text/plain")

		response = self.client.post(
			self.url,
			{"pdf": uploaded_file, "targetChars": '[{"name": "checkbox", "char": "☐"}]'},
			secure=True
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn("Expected a PDF file but got a different file type.", response.content.decode())

	def test_receive_pdf_with_no_file(self):
		response = self.client.post(
			self.url,
			{"targetChars": '[{"name": "checkbox", "char": "☐"}]'},
			secure=True
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn(
			"Either no file uploaded or incorrect form field name",
			response.content.decode()
		)


def pdf_to_binary(file_path: str) -> bytes:
	with open(file_path, "rb") as file:
		return file.read()
	
def get_annotation_rects(pdf_binary: bytes) -> list[pymupdf.Rect]:
	pdf = pymupdf.Document(stream=pdf_binary)
	rects = []

	for page_num in range(len(pdf)):
		page = pdf[page_num]

		for annot in page.annots():
			rects.append(annot.rect)
	
	return rects