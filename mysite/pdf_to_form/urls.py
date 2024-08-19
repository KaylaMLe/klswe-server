from . import views
from django.urls import path


app_name = "pdf-to-form"
urlpatterns = [
	path("", views.receive_pdf, name="receive_pdf"),
]
