from django.contrib import admin
from .models import FavoriteMovie

@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'tmdb_id', 'created_at')
