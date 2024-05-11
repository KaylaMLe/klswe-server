from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()


class Translator:
	def __init__(self):
		self.model = genai.GenerativeModel(model_name="tunedModels/" + os.environ["ACTIVE_MODEL_ID"])

	def translate(self, code: str) -> str:
		typescript_translation = self.model.generate_content(code)
		return typescript_translation.text
