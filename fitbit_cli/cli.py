# -*- coding: utf-8 -*-
"""
CLI Arguments Parser
"""

import argparse
from datetime import datetime, timedelta
import re
from . import __version__


def parse_relative_date(value):
    """Parse relative dates like 'yesterday', 'last-week', 'last-month', 'last-2-days', 'last-2-weeks'."""

    match = re.match(r'^last-(\d+)-(days|weeks|months)$', value, re.IGNORECASE)
    if match:

        number = int(match.group(1))
        unit = match.group(2).lower()

        if unit == "days":
            start_date = datetime.today() - timedelta(days=number)
            end_date = datetime.today()
            return (start_date.date().strftime('%Y-%m-%d'), end_date.date().strftime('%Y-%m-%d'))

        elif unit == "weeks":
            start_date = datetime.today() - timedelta(weeks=number)
            end_date = datetime.today()
            return (start_date.date().strftime('%Y-%m-%d'), end_date.date().strftime('%Y-%m-%d'))

        elif unit == "months":
            # Approximate month by subtracting days (30 days per month for simplicity)
            start_date = datetime.today() - timedelta(days=number * 30)
            end_date = datetime.today()
            return (start_date.date().strftime('%Y-%m-%d'), end_date.date().strftime('%Y-%m-%d'))

    match_simple = re.match(r'^last-(week|month)$', value, re.IGNORECASE)
    if match_simple:
        unit = match_simple.group(1).lower()

        if unit == 'week':
            start_date = datetime.today() - timedelta(weeks=1)
            end_date = datetime.today()
            return (start_date.date().strftime('%Y-%m-%d'), end_date.date().strftime('%Y-%m-%d'))

        elif unit == 'month':

            start_date = datetime.today() - timedelta(days=30)
            end_date = datetime.today()
            return (start_date.date().strftime('%Y-%m-%d'), end_date.date().strftime('%Y-%m-%d'))

    raise argparse.ArgumentTypeError(f"Invalid format: {value}. Use 'yesterday', 'last-week', 'last-month', 'last-N-days', 'last-N-weeks', or 'last-N-months'.")

def parse_date_range(date_str):
    """Date parser that handles both absolute and relative dates"""

    if date_str.lower() == 'yesterday':
        return (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d'), None

    try:
        return (parse_relative_date(date_str))
    except argparse.ArgumentTypeError:
        pass

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
        "Specify date ranges (ISO 8601 format: YYYY-MM-DD) for the following arguments.\n"
        "You can provide a single date or a range (start,end). If not provided, defaults to today's date.",
    )
    group.add_argument(
        "-s",
        "--sleep",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Show sleep data",
    )
    group.add_argument(
        "-o",
        "--spo2",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Show SpO2 data",
    )
    group.add_argument(
        "-e",
        "--heart",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Show Heart Rate Time Series data",
    )
    group.add_argument(
        "-a",
        "--active-zone",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Show Active Zone Minutes (AZM) Time Series data",
    )
    group.add_argument(
        "-b",
        "--breathing-rate",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
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
