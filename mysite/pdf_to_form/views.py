from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import io
import json
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import white
from .target_chars import CHECK_BOX


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def receive_pdf(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		return convert_pdf(request)
	elif request.method == "GET":
		return HttpResponse()
	else:
		return HttpResponse(
			f"Expected GET or POST request but got a {request.method} request.",
			status=405
		)

def convert_pdf(request: HttpRequest) -> HttpResponse:
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

	pdf_data = uploaded_file.read()
	pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
	target_chars = json.loads(request.POST["targetChars"])

	output_pdf_stream = io.BytesIO()
	pdf_writer = PyPDF2.PdfWriter()

	for page_num in range(len(pdf_reader.pages)):
		page = pdf_reader.pages[page_num]
		packet = io.BytesIO()
		can = canvas.Canvas(packet, pagesize=letter)
		can.setFillColor(white)

		for target in target_chars:
			if target["name"] == CHECK_BOX:
				make_widget(can, page_num, target["char"], page)

		can.save()
		packet.seek(0)
		new_pdf = PyPDF2.PdfReader(packet)
		page.merge_page(new_pdf.pages[0])
		pdf_writer.add_page(page)

	pdf_writer.write(output_pdf_stream)
	output_pdf_stream.seek(0)

	return HttpResponse(output_pdf_stream, content_type="application/pdf")

def make_widget(can, page_num: int, target_char: str, page):
	char_instances = page.extract_text().split(target_char)
	for rect_num, _ in enumerate(char_instances[:-1]):
		field_name = CHECK_BOX + "_" + str(page_num) + "_" + str(rect_num)
		# Assuming we have coordinates for the target_char, which we don't in this example
		# You would need to calculate or extract these coordinates
		x0, y0, x1, y1 = 100, 100, 110, 110  # Placeholder coordinates
		diff = ((x1 - x0) - (y1 - y0)) / 2

		if diff > 0:
			x0 += diff
			x1 -= diff
		elif diff < 0:
			y0 += abs(diff)
			y1 -= abs(diff)

		can.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=1)
		can.drawString(x0, y0, field_name)