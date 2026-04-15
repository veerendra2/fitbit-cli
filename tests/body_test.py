# -*- coding: utf-8 -*-
"""
Body CLI Tests
"""

import os
import sys
import unittest
from argparse import Namespace
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# pylint: disable=C0413
from fitbit_cli import formatter as fmt
from fitbit_cli import output
from fitbit_cli.cli import parse_arguments
from fitbit_cli.fitbit_api import FitbitAPI


class TestBodyFeature(unittest.TestCase):
    """Test suite for the unified body time series CLI feature."""

    @patch("sys.argv", ["fitbit-cli", "-B"])
    def test_body_short_flag_parses_successfully(self):
        """Test that -B parses without error and provides a body date argument."""
        args = parse_arguments()
        self.assertIsNotNone(args.body)

    @patch("sys.argv", ["fitbit-cli", "--json", "--body"])
    def test_body_with_json_flag_parses_successfully(self):
        """Test that --body combined with --json parses without error."""
        args = parse_arguments()
        self.assertTrue(args.json)
        self.assertIsNotNone(args.body)

    @patch("sys.argv", ["fitbit-cli", "-b"])
    def test_breathing_rate_short_flag_still_parses_successfully(self):
        """Test that -b remains available for breathing rate after moving body to -B."""
        args = parse_arguments()
        self.assertIsNotNone(args.breathing_rate)

    @patch("sys.argv", ["fitbit-cli", "--breathing-rate"])
    def test_breathing_rate_long_flag_still_parses_successfully(self):
        """Test that --breathing-rate remains available after moving body to -B."""
        args = parse_arguments()
        self.assertIsNotNone(args.breathing_rate)

    def test_get_body_time_series_single_date_uses_period_endpoint(self):
        """Test that a single body date uses the 1d body time series endpoint."""
        fitbit = FitbitAPI("client", "secret", "access", "refresh")
        fitbit.make_request = MagicMock(return_value=MagicMock(json=lambda: {}))

        fitbit.get_body_time_series("weight", "2024-01-05")

        fitbit.make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/body/weight/date/2024-01-05/1d.json",
        )

    def test_get_body_time_series_date_range_uses_range_endpoint(self):
        """Test that a body date range uses the body time series date-range endpoint."""
        fitbit = FitbitAPI("client", "secret", "access", "refresh")
        fitbit.make_request = MagicMock(return_value=MagicMock(json=lambda: {}))

        fitbit.get_body_time_series("bmi", "2024-01-01", "2024-01-07")

        fitbit.make_request.assert_called_once_with(
            "GET",
            "https://api.fitbit.com/1/user/-/body/bmi/date/2024-01-01/2024-01-07.json",
        )

    def test_display_body_as_json_merges_weight_bmi_and_fat_by_date(self):
        """Test that body formatter merges weight, BMI, and fat values into one per-date JSON view."""
        body_data = {
            "weight": {
                "body-weight": [
                    {"dateTime": "2024-01-01", "value": "80.1"},
                    {"dateTime": "2024-01-03", "value": "79.8"},
                ]
            },
            "bmi": {
                "body-bmi": [
                    {"dateTime": "2024-01-01", "value": "24.7"},
                    {"dateTime": "2024-01-02", "value": "24.6"},
                ]
            },
            "fat": {
                "body-fat": [
                    {"dateTime": "2024-01-02", "value": "18.1"},
                    {"dateTime": "2024-01-03", "value": "18.0"},
                ]
            },
        }

        result = fmt.display_body(body_data, as_json=True)

        self.assertEqual(
            result,
            {
                "body": [
                    {
                        "date": "2024-01-01",
                        "weight": "80.1",
                        "bmi": "24.7",
                        "fat": None,
                    },
                    {
                        "date": "2024-01-02",
                        "weight": None,
                        "bmi": "24.6",
                        "fat": "18.1",
                    },
                    {
                        "date": "2024-01-03",
                        "weight": "79.8",
                        "bmi": None,
                        "fat": "18.0",
                    },
                ]
            },
        )

    @patch("fitbit_cli.formatter.CONSOLE.print")
    def test_display_body_table_renders_single_combined_table(self, mock_print):
        """Test that body formatter renders one combined table with weight, BMI, and fat columns."""
        body_data = {
            "weight": {"body-weight": [{"dateTime": "2024-01-01", "value": "80.1"}]},
            "bmi": {"body-bmi": [{"dateTime": "2024-01-01", "value": "24.7"}]},
            "fat": {"body-fat": [{"dateTime": "2024-01-01", "value": "18.1"}]},
        }

        fmt.display_body(body_data)

        table = mock_print.call_args[0][0]
        self.assertEqual(table.title, "Body Time Series :balance_scale:")
        self.assertEqual(len(table.rows), 1)

    def test_json_display_uses_unified_body_formatter(self):
        """Test that json_display fetches body weight, BMI, and fat and returns one unified body payload."""
        fitbit = MagicMock()
        fitbit.get_body_time_series.side_effect = [
            {"body-weight": [{"dateTime": "2024-01-01", "value": "80.1"}]},
            {"body-bmi": [{"dateTime": "2024-01-01", "value": "24.7"}]},
            {"body-fat": [{"dateTime": "2024-01-01", "value": "18.1"}]},
        ]
        args = Namespace(
            user_profile=False,
            devices=False,
            sleep=None,
            spo2=None,
            heart=None,
            active_zone=None,
            breathing_rate=None,
            hrv=None,
            body=("2024-01-01", None),
            activities=None,
        )

        with patch("builtins.print") as mock_print:
            output.json_display(fitbit, args)

        fitbit.get_body_time_series.assert_any_call("weight", "2024-01-01", None)
        fitbit.get_body_time_series.assert_any_call("bmi", "2024-01-01", None)
        fitbit.get_body_time_series.assert_any_call("fat", "2024-01-01", None)
        mock_print.assert_called_once_with(
            '{"body":[{"date":"2024-01-01","weight":"80.1","bmi":"24.7","fat":"18.1"}]}'
        )

    def test_raw_json_display_includes_body_weight_bmi_and_fat_responses(self):
        """Test that raw_json_display includes the three raw body resource responses."""
        fitbit = MagicMock()
        fitbit.get_body_time_series.side_effect = [
            {"body-weight": [{"dateTime": "2026-04-01", "value": "81.5"}]},
            {"body-bmi": [{"dateTime": "2026-04-01", "value": "24.7"}]},
            {"body-fat": [{"dateTime": "2026-04-01", "value": "19.2"}]},
        ]
        args = Namespace(
            user_profile=False,
            devices=False,
            sleep=None,
            spo2=None,
            heart=None,
            active_zone=None,
            breathing_rate=None,
            hrv=None,
            body=("2026-04-01", None),
            activities=None,
        )

        with patch("builtins.print") as mock_print:
            output.raw_json_display(fitbit, args)

        expected_json = (
            '{"body":{"weight":{"body-weight":[{"dateTime":"2026-04-01","value":"81.5"}]},'
            '"bmi":{"body-bmi":[{"dateTime":"2026-04-01","value":"24.7"}]},'
            '"fat":{"body-fat":[{"dateTime":"2026-04-01","value":"19.2"}]}}}'
        )
        mock_print.assert_called_once_with(expected_json)

    @patch("fitbit_cli.output.fmt.display_body")
    def test_table_display_uses_unified_body_formatter(self, mock_display_body):
        """Test that table_display fetches unified body data and renders a single body table."""
        fitbit = MagicMock()
        fitbit.get_body_time_series.side_effect = [
            {"body-weight": [{"dateTime": "2026-04-01", "value": "81.5"}]},
            {"body-bmi": [{"dateTime": "2026-04-01", "value": "24.7"}]},
            {"body-fat": [{"dateTime": "2026-04-01", "value": "19.2"}]},
        ]
        args = Namespace(
            user_profile=False,
            devices=False,
            sleep=None,
            spo2=None,
            heart=None,
            active_zone=None,
            breathing_rate=None,
            hrv=None,
            body=("2026-04-01", None),
            activities=None,
        )

        output.table_display(fitbit, args)

        mock_display_body.assert_called_once_with(
            {
                "weight": {
                    "body-weight": [{"dateTime": "2026-04-01", "value": "81.5"}]
                },
                "bmi": {"body-bmi": [{"dateTime": "2026-04-01", "value": "24.7"}]},
                "fat": {"body-fat": [{"dateTime": "2026-04-01", "value": "19.2"}]},
            }
        )


if __name__ == "__main__":
    unittest.main()
