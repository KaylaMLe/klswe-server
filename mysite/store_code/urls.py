from . import views
from django.urls import path


app_name = "store-code"
urlpatterns = [
	path("", views.store_code_text, name="store_code_text"),
	path("<int:pk>/", views.get_code_text, name="get_code_text"),
	path("<int:pk>/delete/", views.delete_code_text, name="delete_code_text"),
]
