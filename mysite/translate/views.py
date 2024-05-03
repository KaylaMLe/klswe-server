from django.http import HttpRequest, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json
from .gemini.translate import translate
from .models import CodeText


def get_csrf(request: HttpRequest) -> JsonResponse:
	get_token(request)
	return JsonResponse({'detail': 'CSRF cookie set'})

def validate_code_request(request: HttpRequest) -> str | HttpResponse:
	# redirection changes the request method to GET even if the original request was POST
	if request.method != "POST":
		return HttpResponse(
			f"""Expected POST request but got a {request.method} request.
			Did an unexpected redirect occur?
			""",
			status=405
		)
	
	try:
		data = json.loads(request.body.decode("utf-8"))
	except json.JSONDecodeError:
		return HttpResponsBadRequest("Invalid JSON")

	# check if the code is provided
	code = data.get("code")

	if code is None:
		code_msg = ""

		for key in request.POST:
			code_msg += key

		return HttpResponse("Code not provided\n" + code_msg, status=400)
	
	if not code.strip():
		message = "Code is empty." if len(code) == 0 else "Code consists of only whitespace.\n" + code

		return HttpResponse(message, status=400)
	
	return code

def translate_code(request: HttpRequest) -> HttpResponse:
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	return translate(code_or_error)

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
