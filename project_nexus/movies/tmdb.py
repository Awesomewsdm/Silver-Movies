import time
import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

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
        try:
            data = cache.get(cache_key)
        except Exception as e:
            # If cache backend is unavailable, treat as cache miss but log for visibility
            logger.warning('Cache get failed for key %s: %s', cache_key, e)
            data = None

        if data:
            return data

        try:
            data = self._get(f'/trending/{media_type}/{time_window}')
        except Exception:
            # _get will already raise; log and re-raise to let callers handle
            logger.exception('Failed to fetch trending from TMDb')
            raise

        try:
            cache.set(cache_key, data, cache_ttl)
        except Exception as e:
            logger.warning('Cache set failed for key %s: %s', cache_key, e)

        return data

    def get_recommendations(self, tmdb_id, cache_ttl=600):
        cache_key = f'tmdb_recommendations_{tmdb_id}'
        try:
            data = cache.get(cache_key)
        except Exception as e:
            logger.warning('Cache get failed for key %s: %s', cache_key, e)
            data = None

        if data:
            return data

        try:
            data = self._get(f'/movie/{tmdb_id}/recommendations')
        except Exception:
            logger.exception('Failed to fetch recommendations from TMDb for id %s', tmdb_id)
            raise

        try:
            cache.set(cache_key, data, cache_ttl)
        except Exception as e:
            logger.warning('Cache set failed for key %s: %s', cache_key, e)

        return data
