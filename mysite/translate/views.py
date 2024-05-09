from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from .gemini.translate import translate


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

def translate_code(request: HttpRequest) -> HttpResponse:
	csrf_token = get_token(request)
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	return translate(code_or_error)
