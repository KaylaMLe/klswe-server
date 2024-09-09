from django.test import TestCase, Client
from django.urls import reverse
from .models import FormStats, PageStats

class TrafficTrackerTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_increment_form_submissions(self):
		url = "about/contact"
		name = "test_form"
		response = self.client.post(
			reverse("traffic-tracker:increment_form_submissions", args=[url, name]),
			secure=True
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, f"Began tracking submissions for form with {name} on {url}")

		# increment the form submissions
		response = self.client.post(
			reverse("traffic-tracker:increment_form_submissions", args=[url, name]),
			secure=True
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, f"Submissions for form {name} incremented")

		# verify the submissions count
		form_stats = FormStats.objects.get(url=url, name=name)
		self.assertEqual(form_stats.submissions, 2)

	def test_increment_page_views(self):
		url = "about/contact"
		response = self.client.post(
			reverse("traffic-tracker:increment_page_views", args=[url]),
			secure=True
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, f"Began tracking page views for {url}")

		# increment the page views
		response = self.client.post(
			reverse("traffic-tracker:increment_page_views", args=[url]),
			secure=True
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, f"Page views for {url} incremented")

		# verify the page views count
		page_stats = PageStats.objects.get(url=url)
		self.assertEqual(page_stats.views, 2)
