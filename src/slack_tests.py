import unittest
import time
from unittest import mock
from unittest.mock import MagicMock
from requests import Response
from datetime import datetime
from slack import QuoteDownloadService, QuoteOfTheDayService

class QuoteServiceTestCase(unittest.TestCase):
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
        quote_service = QuoteDownloadService()
        quote_service.request('http://localhost')
        mock_request.assert_called_with('http://localhost')

    @mock.patch('slack.requests.get')
    def test_request_returns_list(self, mock_request):
        expected = ['Line 1', 'Line 2', 'Line 3', '# Line 4', 'Line 5', 'Line 6', '# Line 7', 'Line 8']
        mock_request.return_value = MagicMock(spec=Response, status_code=200, text=self.content, content=self.content)
        quote_service = QuoteDownloadService()
        response = quote_service.request('http://localhost')
        self.assertListEqual(response, expected)

    def test_clean_returns_list_without_markdown_and_spaces(self):
        lines = ['Line 1', 'Line 2  ', 'Line 3 ', '# Line 4', 'Line 5', 'Line 6', '# Line 7', 'Line 8']
        quote_service = QuoteDownloadService()
        actual = quote_service.clean(lines)
        expected = ['Line 1', 'Line 2', 'Line 3', 'Line 5', 'Line 6', 'Line 8']
        self.assertListEqual(actual, expected)

class QuoteOfTheDayServiceTestCase(unittest.TestCase):
    def test_day_to_number_returns_number(self):
        date1 = time.strptime('2020-01-01', '%Y-%m-%d')
        date2 = time.strptime('2020-01-02', '%Y-%m-%d')
        date3 = time.strptime('2020-02-03', '%Y-%m-%d')

        day_service = QuoteOfTheDayService()
        self.assertEqual(day_service.day_to_number(date1), 1)
        self.assertEqual(day_service.day_to_number(date2), 2)
        self.assertEqual(day_service.day_to_number(date3), 34)

    @mock.patch('slack.datetime.datetime')
    def test_day_to_number_no_argument_return_today(self, mock_date):
        mock_date.utcnow = MagicMock(return_value=datetime(2020, 1, 4))
        day_service = QuoteOfTheDayService()
        self.assertEqual(day_service.day_to_number(), 4)

    def test_pick_returns_str(self):
        quotes = ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5']
        date1 = time.strptime('2020-01-01', '%Y-%m-%d')
        date2 = time.strptime('2020-01-02', '%Y-%m-%d')
        date3 = time.strptime('2020-01-03', '%Y-%m-%d')
        date4 = time.strptime('2020-01-04', '%Y-%m-%d')
        date5 = time.strptime('2020-01-05', '%Y-%m-%d')

        day_service = QuoteOfTheDayService()
        self.assertEqual(day_service.pick(quotes, date1), 'Line 1')
        self.assertEqual(day_service.pick(quotes, date2), 'Line 2')
        self.assertEqual(day_service.pick(quotes, date3), 'Line 3')
        self.assertEqual(day_service.pick(quotes, date4), 'Line 4')
        self.assertEqual(day_service.pick(quotes, date5), 'Line 5')

    def test_pick_returns_str_should_cycle(self):
        quotes = ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5']
        date1 = time.strptime('2020-01-31', '%Y-%m-%d')
        date2 = time.strptime('2020-02-01', '%Y-%m-%d')
        date3 = time.strptime('2020-02-02', '%Y-%m-%d')
        date4 = time.strptime('2020-02-03', '%Y-%m-%d')
        date5 = time.strptime('2020-02-04', '%Y-%m-%d')

        day_service = QuoteOfTheDayService()
        self.assertEqual(day_service.pick(quotes, date1), 'Line 1')
        self.assertEqual(day_service.pick(quotes, date2), 'Line 2')
        self.assertEqual(day_service.pick(quotes, date3), 'Line 3')
        self.assertEqual(day_service.pick(quotes, date4), 'Line 4')
        self.assertEqual(day_service.pick(quotes, date5), 'Line 5')


if __name__ == "__main__":
    unittest.main()
