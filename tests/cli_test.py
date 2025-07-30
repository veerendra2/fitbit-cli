import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from fitbit_cli.cli import _get_date_range, _parse_relative_dates, parse_date_range


class TestCLIDateFunctions(unittest.TestCase):

    @patch("fitbit_cli.cli.datetime")
    def test_get_date_range(self, mock_datetime):
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test with delta of 7 days
        start_date, end_date = _get_date_range(7)
        self.assertEqual(start_date, "2023-07-23")
        self.assertEqual(end_date, "2023-07-30")

        # Test with delta of 30 days
        start_date, end_date = _get_date_range(30)
        self.assertEqual(start_date, "2023-06-30")
        self.assertEqual(end_date, "2023-07-30")

    @patch("fitbit_cli.cli.datetime")
    def test_parse_relative_dates_yesterday(self, mock_datetime):
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test "yesterday"
        start_date, end_date = _parse_relative_dates("yesterday")
        self.assertEqual(start_date, "2023-07-29")
        self.assertIsNone(end_date)

        # Test with mixed case
        start_date, end_date = _parse_relative_dates("YeStErDaY")
        self.assertEqual(start_date, "2023-07-29")
        self.assertIsNone(end_date)

    @patch("fitbit_cli.cli.datetime")
    def test_parse_relative_dates_last_n(self, mock_datetime):
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test "last-N-days"
        start_date, end_date = _parse_relative_dates("last-5-days")
        self.assertEqual(start_date, "2023-07-25")
        self.assertEqual(end_date, "2023-07-30")

        # Test "last-N-weeks"
        start_date, end_date = _parse_relative_dates("last-2-weeks")
        self.assertEqual(start_date, "2023-07-16")
        self.assertEqual(end_date, "2023-07-30")

        # Test "last-N-months"
        start_date, end_date = _parse_relative_dates("last-1-months")
        self.assertEqual(start_date, "2023-06-30")
        self.assertEqual(end_date, "2023-07-30")

        # Test with mixed case
        start_date, end_date = _parse_relative_dates("LaSt-3-DaYs")
        self.assertEqual(start_date, "2023-07-27")
        self.assertEqual(end_date, "2023-07-30")

    @patch("fitbit_cli.cli.datetime")
    def test_parse_relative_dates_last_period(self, mock_datetime):
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test "last-week"
        start_date, end_date = _parse_relative_dates("last-week")
        self.assertEqual(start_date, "2023-07-23")
        self.assertEqual(end_date, "2023-07-30")

        # Test "last-month"
        start_date, end_date = _parse_relative_dates("last-month")
        self.assertEqual(start_date, "2023-06-30")
        self.assertEqual(end_date, "2023-07-30")

        # Test with mixed case
        start_date, end_date = _parse_relative_dates("LaSt-WeEk")
        self.assertEqual(start_date, "2023-07-23")
        self.assertEqual(end_date, "2023-07-30")

    def test_parse_relative_dates_invalid(self):
        # Test invalid pattern
        result = _parse_relative_dates("invalid-pattern")
        self.assertIsNone(result)

    @patch("fitbit_cli.cli.datetime")
    def test_parse_date_range_relative(self, mock_datetime):
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test relative date pattern
        start_date, end_date = parse_date_range("last-week")
        self.assertEqual(start_date, "2023-07-23")
        self.assertEqual(end_date, "2023-07-30")

    def test_parse_date_range_absolute_single(self):
        # Test single absolute date
        start_date, end_date = parse_date_range("2023-07-15")
        self.assertEqual(start_date, datetime(2023, 7, 15).date())
        self.assertIsNone(end_date)

    def test_parse_date_range_absolute_range(self):
        # Test date range
        start_date, end_date = parse_date_range("2023-07-15,2023-07-20")
        self.assertEqual(start_date, datetime(2023, 7, 15).date())
        self.assertEqual(end_date, datetime(2023, 7, 20).date())

    def test_parse_date_range_invalid_range(self):
        # Test invalid date range (end before start)
        with self.assertRaises(ValueError) as context:
            parse_date_range("2023-07-20,2023-07-15")

        self.assertIn("Start date must not be after end date", str(context.exception))

    def test_parse_date_range_invalid_format(self):
        # Test invalid date format
        with self.assertRaises(ValueError):
            parse_date_range("invalid-date-format")


if __name__ == "__main__":
    unittest.main()
