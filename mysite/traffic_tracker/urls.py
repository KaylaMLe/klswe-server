from . import views
from django.urls import path


app_name = "traffic-tracker"
urlpatterns = [
	path("<path:url>/", views.increment_page_views, name="increment_page_views"),
	path("<int:pk>/", views.increment_form_submissions, name="increment_form_submissions"),
]
