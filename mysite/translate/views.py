from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import CodeText


def store_code_text(request: HttpRequest) -> HttpResponse:
	# redirection changes the request method to GET even if the original request was POST
	if request.method != "POST":
		return HttpResponse(
			f"""Expected POST request but got a {request.method} request.
			Did an unexpected redirect occur?
			""",
			status=405
		)
	
	# check if the code is provided
	if "code" not in request.POST or not request.POST["code"]:
		return HttpResponse("Code not provided", status=400)
	
	if not request.POST["code"].strip():
		return HttpResponse(
			"Code is null, empty, or consists of only whitespace.\n" + request.POST["code"],
			status=400
		)

	code = request.POST.get("code", "")

	code_text = CodeText(code=code)
	code_text.save()

	return HttpResponse("Code saved with id: " + str(code_text.pk))

def get_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	if request.method != "GET":
		return HttpResponse(f"Expected GET request but got a {request.method} request.", status=405)
	
	code_text = get_object_or_404(CodeText, pk=pk)

	return HttpResponse(code_text.code, content_type="text/plain")

def delete_code_text(request: HttpRequest, pk: int) -> HttpResponse:
	if request.method != "DELETE":
		return HttpResponse(f"Expected DELETE request but got a {request.method} request.", status=405)

	code_text = get_object_or_404(CodeText, pk=pk)
	code_text.delete()

	return HttpResponse("Code deleted with id: " + str(pk))
