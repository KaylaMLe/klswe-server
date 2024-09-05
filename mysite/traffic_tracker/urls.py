from . import views
from django.urls import path


app_name = "traffic-tracker"
urlpatterns = [
	path(
		"form/<path:url>/<str:name>/",
		views.increment_form_submissions,
		name="increment_form_submissions"
	),
	path(
		"page/<path:url>/",
		views.increment_page_views,
		name="increment_page_views"
	),
]
