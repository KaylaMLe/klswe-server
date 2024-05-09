from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import CodeText


def validate_code_request(request: HttpRequest) -> str | HttpResponse:
    # redirection changes the request method to GET even if the original request was POST
	if request.method != "POST":
		return HttpResponse(
			f"""Expected POST request but got a {request.method} request.
			Did an unexpected redirect occur?
			""",
			status=405
		)

	# check if the code is provided
	code = request.POST.get("code")

	if code is None:
		code_msg = ""

		for key in request.POST:
			code_msg += key

		return HttpResponse("Code not provided\n" + code_msg, status=400)
	
	if not code.strip():
		message = "Code is empty." if len(code) == 0 else "Code consists of only whitespace.\n" + code

		return HttpResponse(message, status=400)
	
	return code

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
