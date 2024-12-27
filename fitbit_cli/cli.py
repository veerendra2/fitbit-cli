# -*- coding: utf-8 -*-
"""
CLI Arguments Parser
"""

import argparse
from datetime import datetime

from . import __version__


def parse_date_range(date_str):
    """Date parser"""

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
