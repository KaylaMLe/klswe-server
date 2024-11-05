import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import json
import os


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
		except ClientError as e:
			raise e

		# decrypt secret using the associated KMS key and store it in cache
		secret = json.loads(get_secret_value_response['SecretString'])
		cls._secrets_cache[secret_name] = secret

		return secret
