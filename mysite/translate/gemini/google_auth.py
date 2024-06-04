from google.auth import default
from google.auth.transport.requests import Request
import requests

# Obtain ADC credentials
credentials, project = default()

if credentials.expired:
    credentials.refresh(Request())

