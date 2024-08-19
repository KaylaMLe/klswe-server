from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
import pymupdf


target_chars = { "◻": "checkbox" }
checkbox_dim = { "height": 20, "width": 20 }

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

	pdf_data = uploaded_file.read()
	parsed_pdf = pymupdf.Document(stream=pdf_data)

	for page_num in range(len(parsed_pdf)):
		page = parsed_pdf[page_num]

		for target in target_chars:
			char_instances = page.search_for(target)

			for inst in char_instances:
				page.insert_text(inst[:2], " ", fontsize=12)

	return HttpResponse("Success", status=200)
