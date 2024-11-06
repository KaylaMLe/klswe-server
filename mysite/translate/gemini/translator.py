from google.auth import load_credentials_from_file
import google.auth.transport.requests
from dotenv import load_dotenv
import os
import vertexai
from vertexai.generative_models import GenerativeModel

from .system_instruction import system_instruction
from utils.secrets_manager import SecretsManager


load_dotenv()


class Translator:
	def __init__(self):
		# if dev mode is on, use the application default credentials
		credentials = None
		# if dev mode is off (i.e. in production), use the service account credentials
		if os.environ["DEV_MODE"] != "True":
			credentials_path = SecretsManager.get_secret("ProdCredentials")["PATH"]

			credentials, _ = load_credentials_from_file(credentials_path)
			credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

			# request an access token for the GCP service account
			request = google.auth.transport.requests.Request()
			credentials.refresh(request)

		project_id = SecretsManager.get_secret("BEConfig")["GCP_PROJECT_ID"]

		vertexai.init(
			credentials=credentials,
			project=project_id,
			location=os.environ["GCP_REGION"]
		)
		self.model = GenerativeModel(
			model_name=os.environ["MODEL_ID"],
			system_instruction=system_instruction
		)

	def translate(self, code: str) -> str:
		typescript_translation = self.model.generate_content(code)
		return typescript_translation.text
