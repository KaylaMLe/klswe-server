from . import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
	path("admin/", admin.site.urls),
	path("translate/", include("translate.urls")),
	path("store-code/", include("store_code.urls")),
	path("pdf-to-form/", include("pdf_to_form.urls")),
	path("csrf-setter/", include("csrf_setter.urls")),
]

if settings.DEBUG:
	urlpatterns += [
		path("__debug__/", include("debug_toolbar.urls"))
	]
