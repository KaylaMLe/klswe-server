from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import CodeText


def store_code_text(request: HttpRequest) -> HttpResponse:
	code = request.POST.get("code", "")
	code_text = CodeText(code=code)
	code_text.save()

	return HttpResponse("Code saved with id: " + str(code_text.pk))

def get_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	code_text = get_object_or_404(CodeText, pk=pk)

	return HttpResponse(code_text.code, content_type="text/plain")

def delete_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	code_text = get_object_or_404(CodeText, pk=pk)
	code_text.delete()

	return HttpResponse("Code deleted with id: " + str(pk))
