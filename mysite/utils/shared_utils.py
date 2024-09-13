from django.http import HttpRequest, HttpResponse
from functools import wraps
import json


def validate_code_request(request: HttpRequest) -> str | HttpResponse:
	# redirection changes the request method to GET even if the original request was POST
	if request.method != "POST":
		return HttpResponse(
			f"""Expected POST request but got a {request.method} request.
			Did an unexpected redirect occur?
			""",
			status=405
		)

	# load code from json request
	data = json.loads(request.body)
	code = data.get("code")

	# check if the code is provided
	if code is None:
		code_msg = ""

		for key in request.POST:
			code_msg += key

		return HttpResponse("Code not provided\n" + code_msg, status=400)
	
	if not code.strip():
		message = "Code is empty." if len(code) == 0 else "Code consists of only whitespace.\n" + code

		return HttpResponse(message, status=400)
	
	return code

def preflight_handler():
	def decorator(view_func):
		@wraps(view_func)
		def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
			if request.method == "GET":
				return HttpResponse()
			
			return view_func(request, *args, **kwargs)
		return _wrapped_view
	return decorator
