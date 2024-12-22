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

    mutex_group = parser.add_mutually_exclusive_group(required=False)

    mutex_group.add_argument(
        "-d",
        "--json-dump",
        action="store_true",
        help="Dump all your Fitbit data in json files.",
    )
    mutex_group.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Run interative setup to fetch token.",
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
        help="Sleep data",
    )
    group.add_argument(
        "-o",
        "--spo2",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="SpO2 data",
    )
    group.add_argument(
        "-e",
        "--heart",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Heart Rate Time Series",
    )
    group.add_argument(
        "-a",
        "--active-zone",
        type=parse_date_range,
        nargs="?",
        const=(datetime.today().date(), None),
        metavar="DATE[,DATE]",
        help="Active Zone Minutes (AZM) Time Series",
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

    return parser.parse_args()
