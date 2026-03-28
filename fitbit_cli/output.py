# -*- coding: utf-8 -*-
"""
Output modes for the Fitbit CLI
"""

import json
from datetime import datetime, timedelta

from . import formatter as fmt


def collect_activities(fitbit, args):
    """Fetch activity data for a date or date range."""
    start_date, end_date = args.activities
    if end_date is None:
        data = fitbit.get_daily_activity_summary(start_date)
        data["date"] = str(start_date)
        return [data]
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [
        {
            **fitbit.get_daily_activity_summary(
                (start + timedelta(days=i)).strftime("%Y-%m-%d")
            ),
            "date": (start + timedelta(days=i)).strftime("%Y-%m-%d"),
        }
        for i in range((end - start).days + 1)
    ]


def raw_json_display(fitbit, args):
    """Collect API responses and print compact JSON to stdout."""
    result = {}

    if args.user_profile:
        result["user_profile"] = fitbit.get_user_profile()
    if args.devices:
        result["devices"] = fitbit.get_devices()
    if args.sleep:
        result["sleep"] = fitbit.get_sleep_log(*args.sleep)
    if args.spo2:
        result["spo2"] = fitbit.get_spo2_summary(*args.spo2)
    if args.heart:
        result["heart"] = fitbit.get_heart_rate_time_series(*args.heart)
    if args.active_zone:
        result["active_zone"] = fitbit.get_azm_time_series(*args.active_zone)
    if args.breathing_rate:
        result["breathing_rate"] = fitbit.get_breathing_rate_summary(
            *args.breathing_rate
        )
    if args.activities:
        result["activities"] = collect_activities(fitbit, args)

    print(json.dumps(result))


def table_display(fitbit, args):
    """Fetch data and render rich tables to the terminal."""
    with fmt.CONSOLE.status("[bold green]Fetching data...") as _:
        if args.user_profile:
            fmt.display_user_profile(fitbit.get_user_profile())
        if args.devices:
            fmt.display_devices(fitbit.get_devices())
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
        if args.activities:
            activity_data = collect_activities(fitbit, args)
            unit_system = (
                fitbit.get_user_profile().get("user", "").get("distanceUnit", "METRIC")
            )
            fmt.display_activity(activity_data, unit_system)
