from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .models import CustomUser

@never_cache
def register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = CustomUser.objects.create_user(email=email, password=password)
		return JsonResponse({'message': 'User created successfully'}, status=201)

@never_cache
def login_view(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'message': 'Logged in successfully'}, status=200)
		else:
			return JsonResponse({'error': 'Invalid login'}, status=400)

def logout_view(request):
	logout(request)
	return JsonResponse({'message': 'Logged out successfully'}, status=200)