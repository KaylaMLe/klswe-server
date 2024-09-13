from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import FormStats, PageStats
from utils.shared_utils import preflight_handler


@require_http_methods(["POST", "GET"])
@preflight_handler()
def increment_page_views(request: HttpRequest, url: str) -> HttpResponse:
	page_stats, created = PageStats.objects.get_or_create(url=url)

	if created:
		return HttpResponse(f"Began tracking page views for {url}")
	else:
		page_stats.views += 1
		page_stats.save()

		return HttpResponse(f"Page views for {url} incremented")

@require_http_methods(["POST", "GET"])
@preflight_handler()
def increment_form_submissions(request: HttpRequest, url: str, name: str) -> HttpResponse:
	form_stats, created = FormStats.objects.get_or_create(url=url, name=name)
	
	if created:
		return HttpResponse(f"Began tracking submissions for form with {name} on {url}")
	else:
		form_stats.submissions += 1
		form_stats.save()

		return HttpResponse(f"Submissions for form {name} incremented")
