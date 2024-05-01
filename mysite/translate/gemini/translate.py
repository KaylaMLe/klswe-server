from django.http import HttpResponse
import google.generativeai as genai


def translate(code: str) -> HttpResponse:
	model = genai.GenerativeModel(model_name="tunedModels/js-to-ts-model-001")
	typescript_translation = model.generate_content(code)

	return HttpResponse(typescript_translation.text)
