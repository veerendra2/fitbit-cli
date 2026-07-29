# -*- coding: utf-8 -*-
"""
Tests for auto-chunking date ranges > 30 days.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, call

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# pylint: disable=C0413
from fitbit_cli.fitbit_api import FitbitAPI


class TestDateRangeAutoChunking(unittest.TestCase):
    """Test suite for date range auto-chunking (>30 days)."""

    def setUp(self):
        self.api = FitbitAPI("id", "secret", "access", "refresh")
        self.api.make_request = MagicMock()

    def _mock_response(self, json_data):
        mock_resp = MagicMock()
        mock_resp.json.return_value = json_data
        return mock_resp

    def test_single_date(self):
        """Test single date request without end_date."""
        self.api.make_request.return_value = self._mock_response(
            {"br": [{"dateTime": "2023-01-01", "value": {"fullDailyBpms": 15.0}}]}
        )
        res = self.api.get_breathing_rate_summary("2023-01-01")
        self.api.make_request.assert_called_once_with(
            "GET", "https://api.fitbit.com/1/user/-/br/date/2023-01-01.json"
        )
        self.assertEqual(len(res["br"]), 1)

    def test_range_under_30_days(self):
        """Test range <= 30 days."""
        self.api.make_request.return_value = self._mock_response(
            {"hrv": [{"dateTime": "2023-01-01"}, {"dateTime": "2023-01-30"}]}
        )
        res = self.api.get_hrv_summary("2023-01-01", "2023-01-30")
        self.api.make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/hrv/date/2023-01-01/2023-01-30.json",
        )
        self.assertEqual(len(res["hrv"]), 2)

    def test_range_over_30_days_multi_chunk(self):
        """Test range > 30 days resulting in multiple chunk requests."""
        # 2023-01-01 to 2023-02-15 = 45 days diff (chunk 1: Jan 1 to Jan 31 (30 days diff), chunk 2: Feb 1 to Feb 15)
        resp1 = self._mock_response(
            {"br": [{"dateTime": "2023-01-01"}, {"dateTime": "2023-01-31"}]}
        )
        resp2 = self._mock_response(
            {"br": [{"dateTime": "2023-02-01"}, {"dateTime": "2023-02-15"}]}
        )
        self.api.make_request.side_effect = [resp1, resp2]

        res = self.api.get_breathing_rate_intraday("2023-01-01", "2023-02-15")

        expected_calls = [
            call(
                "GET",
                "https://api.fitbit.com/1/user/-/br/date/2023-01-01/2023-01-31/all.json",
            ),
            call(
                "GET",
                "https://api.fitbit.com/1/user/-/br/date/2023-02-01/2023-02-15/all.json",
            ),
        ]
        self.api.make_request.assert_has_calls(expected_calls)
        self.assertEqual(self.api.make_request.call_count, 2)
        self.assertEqual(len(res["br"]), 4)


if __name__ == "__main__":
    unittest.main()
