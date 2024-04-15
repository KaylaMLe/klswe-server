from django.urls import path
from js2ts import views, admin

urlpatterns = [
	path('admin/', admin.my_admin_site.urls),
	path('register/', views.register, name='register'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
]
