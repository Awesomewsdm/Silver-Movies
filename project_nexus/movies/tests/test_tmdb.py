import unittest
from unittest.mock import patch, MagicMock
from movies.tmdb import TMDBClient

class TMDBClientTests(unittest.TestCase):
    @patch('movies.tmdb.requests.Session')
    def test_get_trending_caches_and_returns(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = TMDBClient(api_key='fake')
        data = client.get_trending(cache_ttl=1)
        self.assertIn('results', data)

    @patch('movies.tmdb.requests.Session')
    def test_get_recommendations_calls_api(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': [{'id':1}]}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = TMDBClient(api_key='fake')
        data = client.get_recommendations(123)
        self.assertIn('results', data)

if __name__ == '__main__':
    unittest.main()
