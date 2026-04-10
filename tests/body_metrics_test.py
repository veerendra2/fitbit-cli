# -*- coding: utf-8 -*-
"""
Body Metrics Tests
"""

import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from fitbit_cli import formatter as fmt
from fitbit_cli import output

# pylint: disable=C0413
from fitbit_cli.cli import parse_arguments
from fitbit_cli.fitbit_api import FitbitAPI


class TestBodyMetrics(unittest.TestCase):
    """Test suite for weight and body fat features."""

    @patch("sys.argv", ["fitbit-cli", "--weight"])
    def test_weight_flag_parses_successfully(self):
        """Test that --weight flag parses without error."""
        args = parse_arguments()
        self.assertIsNotNone(args.weight)

    @patch("sys.argv", ["fitbit-cli", "--json", "--body-fat"])
    def test_body_fat_with_json_flag_parses_successfully(self):
        """Test that --body-fat combined with --json parses without error."""
        args = parse_arguments()
        self.assertTrue(args.json)
        self.assertIsNotNone(args.body_fat)

    @patch.object(FitbitAPI, "make_request")
    def test_get_weight_log_calls_expected_endpoint(self, mock_make_request):
        """Test that get_weight_log calls the expected Fitbit endpoint for a single date."""
        mock_make_request.return_value.json.return_value = {"weight": []}

        fitbit = FitbitAPI("client", "secret", "access", "refresh")
        fitbit.get_weight_log("2026-04-01")

        mock_make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/body/log/weight/date/2026-04-01.json",
        )

    @patch.object(FitbitAPI, "make_request")
    def test_get_body_fat_log_calls_expected_endpoint_for_range(
        self, mock_make_request
    ):
        """Test that get_body_fat_log calls the expected Fitbit endpoint for a date range."""
        mock_make_request.return_value.json.return_value = {"fat": []}

        fitbit = FitbitAPI("client", "secret", "access", "refresh")
        fitbit.get_body_fat_log("2026-04-01", "2026-04-07")

        mock_make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/body/log/fat/date/2026-04-01/2026-04-07.json",
        )

    def test_display_weight_returns_expected_json(self):
        """Test that display_weight returns normalized JSON output."""
        result = fmt.display_weight(
            {
                "weight": [
                    {
                        "date": "2026-04-01",
                        "time": "07:15:00",
                        "weight": 81.5,
                        "bmi": 24.7,
                        "source": "Aria",
                    }
                ]
            },
            as_json=True,
        )

        self.assertEqual(
            result,
            {
                "weight": [
                    {
                        "date": "2026-04-01",
                        "time": "07:15:00",
                        "weight": 81.5,
                        "bmi": 24.7,
                    }
                ]
            },
        )

    def test_display_body_fat_returns_expected_json(self):
        """Test that display_body_fat returns normalized JSON output."""
        result = fmt.display_body_fat(
            {
                "fat": [
                    {
                        "date": "2026-04-01",
                        "time": "07:15:00",
                        "fat": 19.2,
                        "source": "Aria",
                    }
                ]
            },
            as_json=True,
        )

        self.assertEqual(
            result,
            {
                "body_fat": [
                    {
                        "date": "2026-04-01",
                        "time": "07:15:00",
                        "fat": 19.2,
                    }
                ]
            },
        )

    def test_json_display_includes_weight_and_body_fat(self):
        """Test that json_display includes both weight and body fat results."""
        fitbit = MagicMock()
        fitbit.get_weight_log.return_value = {
            "weight": [
                {"date": "2026-04-01", "time": "07:15:00", "weight": 81.5, "bmi": 24.7}
            ]
        }
        fitbit.get_body_fat_log.return_value = {
            "fat": [{"date": "2026-04-01", "time": "07:15:00", "fat": 19.2}]
        }
        args = SimpleNamespace(
            user_profile=False,
            devices=False,
            sleep=None,
            spo2=None,
            heart=None,
            active_zone=None,
            breathing_rate=None,
            hrv=None,
            activities=None,
            weight=("2026-04-01", None),
            body_fat=("2026-04-01", None),
        )

        with patch("builtins.print") as mock_print:
            output.json_display(fitbit, args)

        mock_print.assert_called_once_with(
            '{"weight":[{"date":"2026-04-01","time":"07:15:00","weight":81.5,"bmi":24.7}],"body_fat":[{"date":"2026-04-01","time":"07:15:00","fat":19.2}]}'
        )

    def test_raw_json_display_strips_source_from_weight_and_body_fat(self):
        """Test that raw_json_display removes source from weight and body fat output."""
        fitbit = MagicMock()
        fitbit.get_weight_log.return_value = {
            "weight": [
                {
                    "date": "2026-04-01",
                    "time": "07:15:00",
                    "weight": 81.5,
                    "bmi": 24.7,
                    "source": "Aria",
                }
            ]
        }
        fitbit.get_body_fat_log.return_value = {
            "fat": [
                {
                    "date": "2026-04-01",
                    "time": "07:15:00",
                    "fat": 19.2,
                    "source": "Aria",
                }
            ]
        }
        args = SimpleNamespace(
            user_profile=False,
            devices=False,
            sleep=None,
            spo2=None,
            heart=None,
            active_zone=None,
            breathing_rate=None,
            hrv=None,
            activities=None,
            weight=("2026-04-01", None),
            body_fat=("2026-04-01", None),
        )

        with patch("builtins.print") as mock_print:
            output.raw_json_display(fitbit, args)

        mock_print.assert_called_once_with(
            '{"weight":[{"date":"2026-04-01","time":"07:15:00","weight":81.5,"bmi":24.7}],"body_fat":[{"date":"2026-04-01","time":"07:15:00","fat":19.2}]}'
        )


if __name__ == "__main__":
    unittest.main()
