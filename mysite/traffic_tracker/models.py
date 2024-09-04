from django.db import models


class PageStats(models.Model):
	url = models.TextField(primary_key=True)
	views = models.IntegerField()

	def __str__(self):
		return self.url
	
class FormStats(models.Model):
	url = models.URLField()
	name = models.CharField(max_length=100)
	submissions = models.IntegerField()

	def __str__(self):
		return f"{self.url} - {self.name}"
	