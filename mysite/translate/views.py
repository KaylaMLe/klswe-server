from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
import google.generativeai as genai
from utils.shared_utils import validate_code_request


def translate_code(request: HttpRequest) -> HttpResponse:
	csrf_token = get_token(request)
	code_or_error = validate_code_request(request)

	if isinstance(code_or_error, HttpResponse):
		return code_or_error

	model = genai.GenerativeModel(model_name="tunedModels/js-to-ts-model-001")
	typescript_translation = model.generate_content(code_or_error)
	
	return HttpResponse(typescript_translation.text)
