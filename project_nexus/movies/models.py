from django.db import models
from django.conf import settings

class FavoriteMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=255)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id')

    def __str__(self):
        return f"{self.title} ({self.tmdb_id})"
