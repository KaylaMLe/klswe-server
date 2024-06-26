from . import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
	path("admin/", admin.site.urls),
	path("translate/", include("translate.urls")),
	path("store-code/", include("store_code.urls")),
]

if settings.DEBUG:
	urlpatterns += [
		path("__debug__/", include("debug_toolbar.urls"))
	]
