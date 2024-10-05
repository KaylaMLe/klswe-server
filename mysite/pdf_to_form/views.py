from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import io
import json
from math import floor
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, Rect
import PyPDF2
from reportlab.lib import colors, pagesizes
from reportlab.pdfgen import canvas
from . import widget_names
from utils.shared_utils import preflight_handler

@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
@preflight_handler()
def receive_pdf(request: HttpRequest) -> HttpResponse:
	if "pdf" not in request.FILES:
		return HttpResponse(
			"Either no file uploaded or incorrect form field name",
			status=400
		)

	uploaded_file = request.FILES["pdf"]

	if not isinstance(uploaded_file, UploadedFile):
		return HttpResponse(
			"Expected a file but got an unknown type.",
			status=400
		)
	
	if uploaded_file.content_type != "application/pdf":
		return HttpResponse(
			"Expected a PDF file but got a different file type.",
			status=400
		)

	target_chars = json.loads(request.POST["targetChars"])
	pdf_data = uploaded_file.read()
	pdf_writer = parse_pdf(pdf_data, target_chars)

	output_pdf_stream = io.BytesIO()
	pdf_writer.write(output_pdf_stream)
	output_pdf_stream.seek(0)

	return HttpResponse(output_pdf_stream, content_type="application/pdf")

def parse_pdf(pdf_data: bytes, target_chars: list[dict[str, str]]) -> PyPDF2.PdfWriter:
	pdf_bytes = io.BytesIO(pdf_data)
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=pagesizes.letter)

	def make_checkbox(bbox: Rect) -> None:
		x, y, side = square_bbox(bbox)
		name = widget_names.CHECK_BOX + f"_{page_num}_{element_num}"
		can.acroForm.checkbox(
			name=name,
			x=x,
			y=y,
			size=side,
			borderStyle="solid",
			fillColor=colors.white,
			fieldFlags="",
		)

	# match target_chars to the appropriate widget creation function
	target_widgets = {}

	for target in target_chars:
		match target["name"]:
			case widget_names.CHECK_BOX:
				target_widgets[target["char"]] = make_checkbox

	# add widgets to the canvas on the expected pages
	page_num = 0

	for page_layout in extract_pages(pdf_bytes):
		element_num = 0

		for element in page_layout:
			if isinstance(element, (LTTextBox, LTTextLine)):
				for text_line in element:
					if isinstance(text_line, LTTextLine):
						for character in text_line:
							if isinstance(character, LTChar) and character.get_text() in target_widgets:
								target_widgets[character.get_text()](character.bbox)

			element_num += 1

		page_num += 1
		can.showPage()

	# merge the widgets in the canvas with the original PDF
	can.save()
	packet.seek(0)
	new_pdf = PyPDF2.PdfReader(packet)
	original_pdf = PyPDF2.PdfReader(pdf_bytes)

	return merge_pdfs(original_pdf, new_pdf)

def merge_pdfs(pdf1: PyPDF2.PdfReader, pdf2: PyPDF2.PdfReader) -> PyPDF2.PdfWriter:
	output_pdf = PyPDF2.PdfWriter()

	for page_num in range(len(pdf1.pages)):
		page1 = pdf1.pages[page_num]
		page2 = pdf2.pages[page_num]

		page1.merge_page(page2)
		output_pdf.add_page(page1)

	return output_pdf

# outputs the bottom left corner and the side length of a square in the center of the bounding box
def square_bbox(bbox: Rect) -> tuple[int, int, int]:
	x0, y0, x1, y1 = bbox
	side = floor(x1 - x0) # round down because the bbox is larger than the square

	return (round(x0), round(y1 - side), side)
