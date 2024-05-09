import google.generativeai as genai


class Translator:
	def __init__(self):
		self.model = genai.GenerativeModel(model_name="tunedModels/js-to-ts-model-001")

	def translate(self, code: str) -> str:
		typescript_translation = self.model.generate_content(code)
		return typescript_translation.text