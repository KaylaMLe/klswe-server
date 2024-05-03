from . import views
from django.urls import path


app_name = "translate"
urlpatterns = [
	path("csrf/", views.get_csrf, name="csrf"),
    path("code/", views.store_code_text, name="store_code_text"),
	path("code/<int:pk>/", views.get_code_text, name="get_code_text"),
	path("code/<int:pk>/delete/", views.delete_code_text, name="delete_code_text"),
	path("translate/", views.translate_code, name="translate_code")
]
