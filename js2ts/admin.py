from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

class MyAdminSite(admin.AdminSite):
	@never_cache
	@staff_member_required
	def login(self, request, extra_context=None):
			return super().login(request, extra_context)

my_admin_site = MyAdminSite()