from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from utils.shared_utils import preflight_handler, validate_code_request

from utils.vertex_model import VertexModel


system_instruction = """
If the request is not purely Javascript or TypeScript, respond with the request without any modifications.
If the request is purely Javascript or TypeScript, translate the code to TypeScript, adding type annotations as necessary.
Only output the translated code.
Do not add or delete comments, explanations, or formatting.
Do not format the code with markdown.
"""
model = VertexModel(system_instruction=system_instruction)


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
@preflight_handler()
def translate_code(request: HttpRequest) -> HttpResponse:
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	translation = model.get_response(code_or_error)

	return HttpResponse(translation)
