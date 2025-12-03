from django.test import SimpleTestCase, TestCase, override_settings
from unittest.mock import patch, MagicMock
from django.urls import reverse

class ViewsTests(SimpleTestCase):
    @patch('movies.views.TMDBClient')
    def test_trending_view_returns_data(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.get_trending.return_value = {'results': []}
        mock_client_cls.return_value = mock_client

        resp = self.client.get('/api/movies/trending/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.json())

    @patch('movies.views.TMDBClient')
    def test_recommendations_view_returns_data(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.get_recommendations.return_value = {'results': [{'id':2}]}
        mock_client_cls.return_value = mock_client

        resp = self.client.get('/api/movies/123/recommendations/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.json())


@override_settings(DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
})
class AuthTests(TestCase):
    def test_register_and_me(self):
        data = {'username': 'alice', 'password': 'pass123'}
        resp = self.client.post('/api/auth/register/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('access', resp.json())
        token = resp.json()['access']

        # access protected me endpoint
        auth = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        resp2 = self.client.get('/api/auth/me/', **auth)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json()['username'], 'alice')

