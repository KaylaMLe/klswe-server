from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from utils.shared_utils import validate_code_request
from .gemini.translator import Translator


model = Translator()


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def translate_code(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		code_or_error = validate_code_request(request)

		if isinstance(code_or_error, HttpResponse):
			return code_or_error

		translation = model.translate(code_or_error)
		
		return HttpResponse(translation)
	elif request.method == "GET":
		return HttpResponse()
	else:
		return HttpResponse(
			f"Expected GET or POST request but got a {request.method} request.",
			status=405
		)

