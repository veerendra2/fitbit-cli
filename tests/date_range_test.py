# -*- coding: utf-8 -*-
"""
Date Range Chunking Tests for Breathing Rate and HRV APIs
"""

import os
import sys
import unittest
from datetime import date
from unittest.mock import MagicMock

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# pylint: disable=C0413
from fitbit_cli.fitbit_api import FitbitAPI


class TestDateRangeChunking(unittest.TestCase):
    """Test suite for auto-chunking date ranges > 30 days for Breathing Rate and HRV."""

    def setUp(self):
        self.fitbit = FitbitAPI("client", "secret", "access", "refresh")

    def test_breathing_rate_summary_single_date(self):
        """Test breathing rate summary with a single date."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "br": [{"dateTime": "2026-01-01", "value": {"breathingRate": 14.0}}]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_breathing_rate_summary("2026-01-01")

        self.fitbit.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/br/date/2026-01-01.json"
        )
        self.assertEqual(len(res["br"]), 1)

    def test_breathing_rate_summary_short_range(self):
        """Test breathing rate summary with a range <= 30 days."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "br": [{"dateTime": "2026-01-01"}, {"dateTime": "2026-01-15"}]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_breathing_rate_summary("2026-01-01", "2026-01-15")

        self.fitbit.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/br/date/2026-01-01/2026-01-15.json"
        )
        self.assertEqual(len(res["br"]), 2)

    def test_breathing_rate_summary_long_range_chunks_and_aggregates(self):
        """Test breathing rate summary with a range > 30 days automatically chunks and merges data."""
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {
            "br": [{"dateTime": "2026-01-01"}, {"dateTime": "2026-01-30"}]
        }

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = {
            "br": [{"dateTime": "2026-01-31"}, {"dateTime": "2026-03-01"}]
        }

        self.fitbit.make_request = MagicMock(side_effect=[mock_resp1, mock_resp2])

        # Range is 59 days: 2026-01-01 to 2026-03-01
        res = self.fitbit.get_breathing_rate_summary("2026-01-01", "2026-03-01")

        expected_calls = [
            (
                (
                    "GET",
                    "https://api.fitbit.com/1/user/-/br/date/2026-01-01/2026-01-30.json",
                ),
            ),
            (
                (
                    "GET",
                    "https://api.fitbit.com/1/user/-/br/date/2026-01-31/2026-03-01.json",
                ),
            ),
        ]
        self.assertEqual(self.fitbit.make_request.call_args_list, expected_calls)
        self.assertEqual(len(res["br"]), 4)

    def test_breathing_rate_intraday_single_date(self):
        """Test breathing rate intraday with a single date."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "br": [
                {
                    "dateTime": "2026-01-01",
                    "value": {"fullSleepSummaryBreathingRate": 14.5},
                }
            ]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_breathing_rate_intraday("2026-01-01")

        self.fitbit.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/br/date/2026-01-01/all.json"
        )
        self.assertEqual(len(res["br"]), 1)

    def test_breathing_rate_intraday_short_range(self):
        """Test breathing rate intraday with a range <= 30 days."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "br": [{"dateTime": "2026-01-01"}, {"dateTime": "2026-01-20"}]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_breathing_rate_intraday("2026-01-01", "2026-01-20")

        self.fitbit.make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/br/date/2026-01-01/2026-01-20/all.json",
        )
        self.assertEqual(len(res["br"]), 2)

    def test_breathing_rate_intraday_long_range_chunks_and_aggregates(self):
        """Test breathing rate intraday with a range > 30 days automatically chunks and merges data."""
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {
            "br": [{"dateTime": "2026-01-01"}, {"dateTime": "2026-01-30"}]
        }

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = {
            "br": [{"dateTime": "2026-01-31"}, {"dateTime": "2026-02-15"}]
        }

        self.fitbit.make_request = MagicMock(side_effect=[mock_resp1, mock_resp2])

        res = self.fitbit.get_breathing_rate_intraday("2026-01-01", "2026-02-15")

        expected_calls = [
            (
                (
                    "GET",
                    "https://api.fitbit.com/1/user/-/br/date/2026-01-01/2026-01-30/all.json",
                ),
            ),
            (
                (
                    "GET",
                    "https://api.fitbit.com/1/user/-/br/date/2026-01-31/2026-02-15/all.json",
                ),
            ),
        ]
        self.assertEqual(self.fitbit.make_request.call_args_list, expected_calls)
        self.assertEqual(len(res["br"]), 4)

    def test_hrv_summary_single_date(self):
        """Test HRV summary with a single date."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "hrv": [{"dateTime": "2026-01-01", "value": {"dailyRmssd": 42.0}}]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_hrv_summary("2026-01-01")

        self.fitbit.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/hrv/date/2026-01-01.json"
        )
        self.assertEqual(len(res["hrv"]), 1)

    def test_hrv_summary_short_range(self):
        """Test HRV summary with a range <= 30 days."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "hrv": [{"dateTime": "2026-01-01"}, {"dateTime": "2026-01-25"}]
        }
        self.fitbit.make_request = MagicMock(return_value=mock_resp)

        res = self.fitbit.get_hrv_summary("2026-01-01", "2026-01-25")

        self.fitbit.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/hrv/date/2026-01-01/2026-01-25.json"
        )
        self.assertEqual(len(res["hrv"]), 2)

    def test_hrv_long_range_chunks_and_aggregates(self):
        """Test HRV summary with a range > 30 days automatically chunks and merges data."""
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {"hrv": [{"dateTime": "2026-01-01"}]}

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = {"hrv": [{"dateTime": "2026-01-31"}]}

        self.fitbit.make_request = MagicMock(side_effect=[mock_resp1, mock_resp2])

        res = self.fitbit.get_hrv_summary(date(2026, 1, 1), date(2026, 3, 1))

        self.assertEqual(self.fitbit.make_request.call_count, 2)
        self.assertEqual(len(res["hrv"]), 2)


if __name__ == "__main__":
    unittest.main()
