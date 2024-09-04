from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def set_csrf_cookie(request: HttpRequest) -> HttpResponse:
	return HttpResponse(status=204)
