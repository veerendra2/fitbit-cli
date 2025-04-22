# -*- coding: utf-8 -*-
"""
CLI Arguments Parser
"""

import argparse
from datetime import datetime, timedelta
import re
from . import __version__


def _get_date_range(delta_days):
    start_date = datetime.today() - timedelta(days=delta_days)
    end_date = datetime.today()
    return (
        start_date.date().strftime("%Y-%m-%d"),
        end_date.date().strftime("%Y-%m-%d"),
    )


def parse_date_range(date_str):
    """Date parser that handles both absolute and relative dates"""

    if date_str.lower() == "yesterday":
        return (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d"), None

    match = re.match(r"^last-(\d+)-(days|weeks|months)$", date_str, re.IGNORECASE)
    if match:
        number = int(match.group(1))
        unit = match.group(2).lower()

        if unit == "days":
            return _get_date_range(number)
        elif unit == "weeks":
            return _get_date_range(number * 7)
        elif unit == "months":
            return _get_date_range(number * 30)

    match_simple = re.match(r"^last-(week|month)$", date_str, re.IGNORECASE)
    if match_simple:
        unit = match_simple.group(1).lower()

        if unit == "week":
            return _get_date_range(7)
        elif unit == "month":
            return _get_date_range(30)

    dates = date_str.split(",")
    start_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
    try:
        end_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
        if start_date > end_date:
            raise ValueError("Start date must not be after end date")
    except IndexError:
        end_date = None

    return (start_date, end_date)


def parse_arguments():
    """Argument parser"""

    parser = argparse.ArgumentParser(
        description="Fitbit CLI -- Access your Fitbit data at your terminal.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--init-auth",
        action="store_true",
        help="Initialize Fitbit iterative authentication setup",
    )

    group = parser.add_argument_group(
        "APIs",
        "Specify a date, date range (YYYY-MM-DD[,YYYY-MM-DD]), or relative date.\n"
        "Relative dates: yesterday, last-week, last-month, last-N-days/weeks/months (e.g., last-2-days).\n"
        "If not provided, defaults to today's date.",
    )
    group.add_argument(
        "-s",
        "--sleep",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]|RELATIVE",
        help="Show sleep data",
    )
    group.add_argument(
        "-o",
        "--spo2",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]|RELATIVE",
        help="Show SpO2 data",
    )
    group.add_argument(
        "-e",
        "--heart",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]|RELATIVE",
        help="Show Heart Rate Time Series data",
    )
    group.add_argument(
        "-a",
        "--active-zone",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]|RELATIVE",
        help="Show Active Zone Minutes (AZM) Time Series data",
    )
    group.add_argument(
        "-b",
        "--breathing-rate",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]|RELATIVE",
        help="Show Breathing Rate Summary data",
    )
    group.add_argument(
        "-u",
        "--show-user-profile",
        action="store_true",
        help="Show user profile data",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
        help="Show fitbit-cli version",
    )

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.error("No arguments provided. At least one argument is required.")

    return args
