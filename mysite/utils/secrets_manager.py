import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import traceback


load_dotenv()


class SecretsManager:
	_client = None
	_secrets_cache = {}

	@classmethod
	def get_client(cls):
		"""Create and return a singleton client for AWS Secrets Manager."""

		if cls._client is None:
			cls._client = boto3.client("secretsmanager", region_name=os.environ["AWS_REGION"])

		return cls._client

	@classmethod
	def get_secret(cls, secret_name):
		"""Retrieve and cache secret value from Secrets Manager by name."""

		if secret_name in cls._secrets_cache:
			return cls._secrets_cache[secret_name]

		client = cls.get_client()

		try:
			get_secret_value_response = client.get_secret_value(SecretId=secret_name)
		except ClientError:
			current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			log_filename = f"error_log_{current_time}.txt"

			# write to a file to avoid printing sensitive information to the console
			with open(os.path.join(os.environ["LOG_PATH"], log_filename), "a") as f:
				f.write(f"{traceback.format_exc()}\n")

			raise RuntimeError(
				f"A ClientError occurred while retrieving secret {secret_name}. "
				"Check {log_filename} for more details."
			)

		# decrypt secret using the associated KMS key and store it in cache
		secret = json.loads(get_secret_value_response['SecretString'])
		cls._secrets_cache[secret_name] = secret

		return secret
