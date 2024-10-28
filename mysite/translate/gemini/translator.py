from dotenv import load_dotenv
import os
import vertexai
from vertexai.generative_models import GenerativeModel

from .system_instruction import system_instruction


load_dotenv()


class Translator:
	def __init__(self):
		vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["REGION"])

		self.model = GenerativeModel(model_name=os.environ["MODEL_ID"], system_instruction=system_instruction)

	def translate(self, code: str) -> str:
		typescript_translation = self.model.generate_content(code)
		return typescript_translation.text
