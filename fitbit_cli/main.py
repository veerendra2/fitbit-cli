# -*- coding: utf-8 -*-
"""
Main Module
"""

import json
import sys

from . import formatter
from .cli import parse_arguments
from .fitbit_api import FitbitAPI
from .fitbit_init import FITBIT_TOKEN_PATH, fitbit_init_setup


def main():
    """Main function"""

    args = parse_arguments()

    if args.init:
        fitbit_init_setup()

    try:
        with open(FITBIT_TOKEN_PATH, encoding="utf-8") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        formatter.CONSOLE.print(
            ":grimacing: Fitbit token file not found. "
            "If this is your first time running the CLI, use '--init' argument to set up the token.",
            style="bold red",
        )
        sys.exit(1)

    fitbit = FitbitAPI(
        client_id=credentials["client_id"],
        client_secret=credentials["secret"],
        access_token=credentials["access_token"],
        refresh_token=credentials["refresh_token"],
    )

    with formatter.CONSOLE.status("[bold green]Fetching data...") as _:
        if args.show_user_profile:
            formatter.display_user_profile(fitbit.get_user_profile())
        if args.sleep:
            formatter.display_sleep(fitbit.get_sleep_log(*args.sleep))
        if args.spo2:
            formatter.display_spo2(fitbit.get_spo2_summary(*args.spo2))
        if args.heart:
            formatter.display_heart_data(fitbit.get_heart_rate_time_series(*args.heart))
        if args.active_zone:
            formatter.display_azm_time_series(
                fitbit.get_azm_time_series(*args.active_zone)
            )
