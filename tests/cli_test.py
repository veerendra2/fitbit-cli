# -*- coding: utf-8 -*-
"""
CLI Tests
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# pylint: disable=C0413
from fitbit_cli.cli import (
    _get_date_range,
    _parse_relative_dates,
    parse_arguments,
    parse_date_range,
)


class TestCLIDateFunctions(unittest.TestCase):
    """Test suite for date-related utility functions in the fitbit_cli.cli module."""

    @patch("fitbit_cli.cli.datetime")
    def test_get_date_range(self, mock_datetime):
        """Test the _get_date_range function calculates correct date ranges based on day deltas."""
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
        """Test the _parse_relative_dates function correctly handles 'yesterday' keyword regardless of case."""
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
        """Test the _parse_relative_dates function correctly handles 'last-N-days/weeks/months' patterns."""
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
        """Test the _parse_relative_dates function correctly handles 'last-week/month' patterns."""
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
        """Test the _parse_relative_dates function returns None for invalid date patterns."""
        # Test invalid pattern
        result = _parse_relative_dates("invalid-pattern")
        self.assertIsNone(result)

    @patch("fitbit_cli.cli.datetime")
    def test_parse_date_range_relative(self, mock_datetime):
        """Test the parse_date_range function correctly handles relative date patterns."""
        # Mock today's date to be 2023-07-30
        mock_today = datetime(2023, 7, 30)
        mock_datetime.today.return_value = mock_today

        # Test relative date pattern
        start_date, end_date = parse_date_range("last-week")
        self.assertEqual(start_date, "2023-07-23")
        self.assertEqual(end_date, "2023-07-30")

    def test_parse_date_range_absolute_single(self):
        """Test the parse_date_range function correctly handles a single absolute date."""
        # Test single absolute date
        start_date, end_date = parse_date_range("2023-07-15")
        self.assertEqual(start_date, datetime(2023, 7, 15).date())
        self.assertIsNone(end_date)

    def test_parse_date_range_absolute_range(self):
        """Test the parse_date_range function correctly handles an absolute date range."""
        # Test date range
        start_date, end_date = parse_date_range("2023-07-15,2023-07-20")
        self.assertEqual(start_date, datetime(2023, 7, 15).date())
        self.assertEqual(end_date, datetime(2023, 7, 20).date())

    def test_parse_date_range_invalid_range(self):
        """Test the parse_date_range function raises ValueError when end date is before start date."""
        # Test invalid date range (end before start)
        with self.assertRaises(ValueError) as context:
            parse_date_range("2023-07-20,2023-07-15")

        self.assertIn("Start date must not be after end date", str(context.exception))

    def test_parse_date_range_invalid_format(self):
        """Test the parse_date_range function raises ValueError for invalid date formats."""
        # Test invalid date format
        with self.assertRaises(ValueError):
            parse_date_range("invalid-date-format")

    @patch("sys.argv", ["fitbit-cli", "--json"])
    def test_json_flag_alone_raises_error(self):
        """Test that --json alone (without a data flag) triggers the no-arguments error."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch("sys.argv", ["fitbit-cli", "--raw-json"])
    def test_raw_json_flag_alone_raises_error(self):
        """Test that --raw-json alone (without a data flag) triggers the no-arguments error."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch("sys.argv", ["fitbit-cli", "--json", "--user-profile"])
    def test_json_with_data_flag_parses_successfully(self):
        """Test that --json combined with a data flag parses without error."""
        args = parse_arguments()
        self.assertTrue(args.json)
        self.assertTrue(args.user_profile)

    @patch("sys.argv", ["fitbit-cli", "--raw-json", "--devices"])
    def test_raw_json_with_data_flag_parses_successfully(self):
        """Test that --raw-json combined with a data flag parses without error."""
        args = parse_arguments()
        self.assertTrue(args.raw_json)
        self.assertTrue(args.devices)

    @patch("sys.argv", ["fitbit-cli", "--init-auth"])
    def test_init_auth_alone_parses_successfully(self):
        """Test that --init-auth alone does not trigger the no-arguments error."""
        args = parse_arguments()
        self.assertTrue(args.init_auth)

    @patch("sys.argv", ["fitbit-cli", "--hrv"])
    def test_hrv_flag_parses_successfully(self):
        """Test that --hrv flag parses without error."""
        args = parse_arguments()
        self.assertIsNotNone(args.hrv)

    @patch("sys.argv", ["fitbit-cli", "--json", "--hrv"])
    def test_hrv_with_json_flag_parses_successfully(self):
        """Test that --hrv combined with --json parses without error."""
        args = parse_arguments()
        self.assertTrue(args.json)
        self.assertIsNotNone(args.hrv)

    @patch("sys.argv", ["fitbit-cli", "--raw-json", "--hrv"])
    def test_hrv_with_raw_json_flag_parses_successfully(self):
        """Test that --hrv combined with --raw-json parses without error."""
        args = parse_arguments()
        self.assertTrue(args.raw_json)
        self.assertIsNotNone(args.hrv)

    @patch("sys.argv", ["fitbit-cli", "--hrv", "2024-01-01"])
    def test_hrv_with_single_date_parses_successfully(self):
        """Test that --hrv with a single date parses without error."""
        args = parse_arguments()
        self.assertIsNotNone(args.hrv)

    @patch("sys.argv", ["fitbit-cli", "--hrv", "2024-01-01,2024-01-07"])
    def test_hrv_with_date_range_parses_successfully(self):
        """Test that --hrv with a date range parses without error."""
        args = parse_arguments()
        self.assertIsNotNone(args.hrv)

    @patch("sys.argv", ["fitbit-cli", "--hrv", "last-week"])
    def test_hrv_with_relative_date_parses_successfully(self):
        """Test that --hrv with a relative date parses without error."""
        args = parse_arguments()
        self.assertIsNotNone(args.hrv)


if __name__ == "__main__":
    unittest.main()
