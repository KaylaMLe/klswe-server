from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import io
import json
import pymupdf
from .target_chars import target_chars, CHECK_BOX


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
	parsed_pdf = pymupdf.Document(stream=pdf_data)
	target_chars = json.loads(request.POST["targetChars"])

	for page_num in range(len(parsed_pdf)):
		page = parsed_pdf[page_num]

		for target in target_chars:
			match target["name"]:
				case CHECK_BOX:
					make_widget = make_checkbox

			char_instances = page.search_for(target["char"])

			for rect_num in range(len(char_instances)):
				page.draw_rect(char_instances[rect_num], color=(1, 1, 1), fill=(1, 1, 1))
				page.add_widget(make_widget(page_num, rect_num, char_instances))

	output_binary = io.BytesIO()
	parsed_pdf.save(output_binary)
	output_binary.seek(0)
	parsed_pdf.close()

	return HttpResponse(output_binary, content_type="application/pdf")

def make_checkbox(page_num: int, rect_num: int, instances: list[pymupdf.Rect]) -> pymupdf.Widget:
	field_name = CHECK_BOX + "_" + str(page_num) + "_" + str(rect_num)

	[x0, y0, x1, y1] = instances[rect_num][:4]
	diff = ((x1 - x0) - (y1 - y0)) / 2

	# if the rectangle is wider than it is tall
	if diff > 0:
		x0 += diff
		x1 -= diff
	# if the rectangle is taller than it is wide
	elif diff < 0:
		y0 += abs(diff)
		y1 -= abs(diff)

	rect = pymupdf.Rect(x0=x0, y0=y0, x1=x1, y1=y1)

	widget = pymupdf.Widget()
	widget.field_name = field_name
	widget.rect = rect
	widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX

	widget.border_width = 1
	widget.border_color = (0, 0, 0)

	return widget
