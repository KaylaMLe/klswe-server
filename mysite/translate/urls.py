from . import views
from django.urls import path


app_name = "translate"
urlpatterns = [
	path("", views.translate_code, name="translate_code")
]
