from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import health, entries_cards, entries_posts, entries_all


urlpatterns = [
    path("admin/", admin.site.urls),

    path("health/", health),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    path("entries/cards/", entries_cards),
    path("entries/posts/", entries_posts),
    path("entries/all/", entries_all),
]
