from google.auth import load_credentials_from_file
import google.auth.transport.requests
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import os


load_dotenv()
# if dev mode is on, use the application default credentials
credentials = None
# if dev mode is off (i.e. in production), use the service account credentials
if os.environ["DEV_MODE"] != "True":
	credentials, project_id = load_credentials_from_file(os.environ["CREDENTIALS_PATH"])
	credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

	# request an access token for the GCP service account
	request = google.auth.transport.requests.Request()
	credentials.refresh(request)

vertexai.init(credentials=credentials, project=os.environ["PROJECT_ID2"], location=os.environ["REGION"])
model = GenerativeModel(model_name=os.environ["MODEL_ID"])

response = model.generate_content("Hi!")
print(response.text)
