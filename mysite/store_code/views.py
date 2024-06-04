from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import CodeText
from utils.shared_utils import validate_code_request


def store_code_text(request: HttpRequest) -> HttpResponse:
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	code_text = CodeText(code=code_or_error)
	code_text.save()

	return HttpResponse("Code saved with id: " + str(code_text.pk))

def get_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	if request.method != "GET":
		return HttpResponse(f"Expected GET request but got a {request.method} request.", status=405)
	
	code_text = get_object_or_404(CodeText, pk=pk)

	return HttpResponse(code_text.code, content_type="text/plain")

def delete_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	if request.method != "DELETE":
		return HttpResponse(f"Expected DELETE request but got a {request.method} request.", status=405)

	code_text = get_object_or_404(CodeText, pk=pk)
	code_text.delete()

	return HttpResponse("Code deleted with id: " + str(pk))
