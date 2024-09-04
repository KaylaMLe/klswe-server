from . import views
from django.urls import path


app_name = "csrf-setter"
urlpatterns = [
	path("", views.set_csrf_cookie, name="set_csrf_cookie"),
]
