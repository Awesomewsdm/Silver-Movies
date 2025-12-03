import time
import requests
from django.conf import settings
from django.core.cache import cache

class TMDBClient:
    BASE_URL = 'https://api.themoviedb.org/3'

    def __init__(self, api_key=None, session=None):
        self.api_key = api_key or getattr(settings, 'TMDB_API_KEY', None)
        self.session = session or requests.Session()

    def _get(self, path, params=None, retries=2, backoff=0.5):
        if not self.api_key:
            raise RuntimeError('TMDB API key not configured')
        params = params or {}
        params['api_key'] = self.api_key
        url = f'{self.BASE_URL}{path}'
        attempt = 0
        while True:
            try:
                resp = self.session.get(url, params=params, timeout=6)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException:
                attempt += 1
                if attempt > retries:
                    raise
                time.sleep(backoff * attempt)

    def get_trending(self, media_type='movie', time_window='week', cache_ttl=600):
        cache_key = f'tmdb_trending_{media_type}_{time_window}'
        data = cache.get(cache_key)
        if data:
            return data
        data = self._get(f'/trending/{media_type}/{time_window}')
        cache.set(cache_key, data, cache_ttl)
        return data

    def get_recommendations(self, tmdb_id, cache_ttl=600):
        cache_key = f'tmdb_recommendations_{tmdb_id}'
        data = cache.get(cache_key)
        if data:
            return data
        data = self._get(f'/movie/{tmdb_id}/recommendations')
        cache.set(cache_key, data, cache_ttl)
        return data
