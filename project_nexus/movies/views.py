from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import FavoriteMovie
from .serializers import UserSerializer, FavoriteMovieSerializer
from django.conf import settings
from django.core.cache import cache
from .tmdb import TMDBClient
import logging

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'status': 'ok'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=response.data['id'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': response.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)

class TrendingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        client = TMDBClient()
        try:
            data = client.get_trending()
            return Response(data)
        except RuntimeError as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            logger.exception('Trending endpoint failed')
            return Response({'detail': 'Failed to fetch trending from TMDb'}, status=status.HTTP_502_BAD_GATEWAY)

class RecommendationsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, tmdb_id: int):
        client = TMDBClient()
        try:
            data = client.get_recommendations(tmdb_id)
            return Response(data)
        except RuntimeError as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            logger.exception('Recommendations endpoint failed for id %s', tmdb_id)
            return Response({'detail': 'Failed to fetch recommendations from TMDb'}, status=status.HTTP_502_BAD_GATEWAY)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
