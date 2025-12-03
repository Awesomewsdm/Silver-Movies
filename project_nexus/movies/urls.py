from django.urls import path
from .views import HealthCheckView, RegisterView, FavoriteListCreateView, FavoriteDetailView, TrendingView, RecommendationsView, MeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorites_list_create'),
    path('favorites/<int:pk>/', FavoriteDetailView.as_view(), name='favorites_detail'),
    path('movies/trending/', TrendingView.as_view(), name='trending'),
    path('movies/<int:tmdb_id>/recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
