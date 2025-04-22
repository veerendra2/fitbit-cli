# -*- coding: utf-8 -*-
"""
Main Module
"""

from . import fitbit_setup as setup
from . import formatter as fmt
from .cli import parse_arguments
from .fitbit_api import FitbitAPI


def main():
    """Main function"""

    args = parse_arguments()

    if args.init_auth:
        setup.fitbit_init_setup()

    credentials = setup.read_fitbit_token()

    fitbit = FitbitAPI(
        client_id=credentials["client_id"],
        client_secret=credentials["secret"],
        access_token=credentials["access_token"],
        refresh_token=credentials["refresh_token"],
    )

    with fmt.CONSOLE.status("[bold green]Fetching data...") as _:
        if args.show_user_profile:
            fmt.display_user_profile(fitbit.get_user_profile())
        if args.sleep:
            fmt.display_sleep(fitbit.get_sleep_log(*args.sleep))
        if args.spo2:
            fmt.display_spo2(fitbit.get_spo2_summary(*args.spo2))
        if args.heart:
            fmt.display_heart_data(fitbit.get_heart_rate_time_series(*args.heart))
        if args.active_zone:
            fmt.display_azm_time_series(fitbit.get_azm_time_series(*args.active_zone))
        if args.breathing_rate:
            fmt.display_breathing_rate(
                fitbit.get_breathing_rate_summary(*args.breathing_rate)
            )
