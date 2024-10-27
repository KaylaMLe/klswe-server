from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()


class Translator:
	def __init__(self):
		genai.configure(api_key=os.environ["GEMINI_API_KEY"])

		for model_info in genai.list_tuned_models():
			print("*")
			print(model_info.name)

		self.model = genai.GenerativeModel("gemini-1.5-flash")

	def translate(self, code: str) -> str:
		typescript_translation = self.model.generate_content(code)
		return typescript_translation.text
