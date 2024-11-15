from datetime import datetime, timedelta, timezone
from google.auth import load_credentials_from_file
from google.auth.credentials import Credentials
import google.auth.transport.requests
from dotenv import load_dotenv
import os
from typing import Optional
import vertexai
from vertexai.generative_models import GenerativeModel

from utils.secrets_manager import SecretsManager


load_dotenv()


class VertexModel:
	def __init__(self, system_instruction: Optional[str]) -> None:
		self.system_instruction = system_instruction

		# if dev mode is on, use the application default credentials
		credentials = None

		# if dev mode is off (i.e. in production), use the service account credentials
		if os.environ["DEV_MODE"] != "True":
			credentials = self._refresh_creds()

		# set initial expiry time if service account credentials are used
		self.expiry = credentials.expiry if credentials else None
		self._initialize_model(credentials)

	def _initialize_model(self, creds: Optional[Credentials]) -> None:
		project_id = SecretsManager.get_secret("klswe-be/shared/gcp_config")["PROJECT_ID"]

		vertexai.init(
			credentials=creds,
			project=project_id,
			location=os.environ["GCP_REGION"]
		)
		self.model = GenerativeModel(
			model_name=os.environ["MODEL_ID"],
			system_instruction=self.system_instruction
		)

	def _refresh_creds(self) -> Credentials:
		credentials_path = SecretsManager.get_secret("klswe-be/prod/gcp_creds")["PATH"]

		credentials, _ = load_credentials_from_file(credentials_path)
		credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

		# request an access token for the GCP service account
		request = google.auth.transport.requests.Request()
		credentials.refresh(request)
		self.expiry = credentials.expiry

		return credentials

	def _reinit(self) -> None:
		# if the creds will expire within a minute
		if self.expiry and self.expiry < datetime.now() + timedelta(seconds=60):
			credentials = self._refresh_creds()
			self.expiry = credentials.expiry
			self._initialize_model(credentials)

	def get_response(self, prompt: str) -> str:
		self._reinit()
		return self.model.generate_content(prompt).text
