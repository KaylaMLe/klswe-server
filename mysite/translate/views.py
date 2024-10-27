from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from utils.shared_utils import preflight_handler, validate_code_request
from .gemini.translator import Translator


model = Translator()


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
@preflight_handler()
def translate_code(request: HttpRequest) -> HttpResponse:
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	translation = model.translate(code_or_error)

	return HttpResponse(translation)
