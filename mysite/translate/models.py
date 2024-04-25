from django.db import models


class CodeText(models.Model):
	code = models.TextField()

	def __str__(self):
		return self.code[:50].strip()
