import unittest
import time
from unittest import mock
from unittest.mock import MagicMock
from requests import Response
from datetime import datetime
from slack import download_quotes, remove_markdown_heading_spaces, pick_quote_for_today

class QuoteTestCase(unittest.TestCase):
    def setUp(self):
        self.content = """Line 1
Line 2
Line 3
# Line 4
Line 5
Line 6
# Line 7
Line 8"""

    @mock.patch('slack.requests.get')
    def test_request_calls_get(self, mock_request):
        mock_request.return_value = MagicMock(spec=Response, status_code=200, text=self.content, content=self.content)
        download_quotes('http://localhost')
        mock_request.assert_called_with('http://localhost')

    @mock.patch('slack.requests.get')
    def test_download_quotes_returns_str(self, mock_request):
        expected = ['Line 1', 'Line 2', 'Line 3', '# Line 4', 'Line 5', 'Line 6', '# Line 7', 'Line 8']
        mock_request.return_value = MagicMock(spec=Response, status_code=200, text=self.content, content=self.content)
        response = download_quotes('http://localhost')
        self.assertEqual(response, self.content)

    def test_remove_markdown_heading_spaces_returns_list(self):
        actual = remove_markdown_heading_spaces(self.content)
        expected = ['Line 1', 'Line 2', 'Line 3', 'Line 5', 'Line 6', 'Line 8']
        self.assertListEqual(actual, expected)

    @mock.patch('slack.datetime.datetime')
    def test_pick_quote_for_1st_jan(self, mock_date):
        mock_date.utcnow = MagicMock(return_value=datetime(2020, 1, 1))
        quotes = remove_markdown_heading_spaces(self.content)
        actual = pick_quote_for_today(quotes)
        self.assertEqual(actual, "Line 1")

    @mock.patch('slack.datetime.datetime')
    def test_pick_quote_for_2nd_jan(self, mock_date):
        mock_date.utcnow = MagicMock(return_value=datetime(2020, 1, 2))
        quotes = remove_markdown_heading_spaces(self.content)
        actual = pick_quote_for_today(quotes)
        self.assertEqual(actual, "Line 2")

    @mock.patch('slack.datetime.datetime')
    def test_pick_quote_for_2nd_feb(self, mock_date):
        mock_date.utcnow = MagicMock(return_value=datetime(2020, 2, 2))
        quotes = remove_markdown_heading_spaces(self.content)
        actual = pick_quote_for_today(quotes)
        self.assertEqual(actual, "Line 3")

if __name__ == "__main__":
    unittest.main()
