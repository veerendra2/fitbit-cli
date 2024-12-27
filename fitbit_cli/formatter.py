# -*- coding: utf-8 -*-
"""
Json Data Formatter
"""
from rich.console import Console
from rich.table import Table

CONSOLE = Console()


def display_user_profile(user_data):
    """User data formatter"""

    user = user_data["user"]
    height_unit = "cm" if user["heightUnit"] == "METRIC" else "in"
    weight_unit = "kg" if user["weightUnit"] == "METRIC" else "lb"

    table = Table(title=f"Hello, {user['displayName']} :wave:", show_header=False)

    table.add_column("")
    table.add_column("")

    table.add_row(":bust_in_silhouette: First Name", user["firstName"])
    table.add_row(":family: Last Name", user["lastName"])
    table.add_row(":birthday: Date Of Birth", user["dateOfBirth"])
    table.add_row(":hourglass_flowing_sand: Age", str(user["age"]))
    table.add_row(":restroom: Gender", user["gender"])
    table.add_row(":straight_ruler: Height", f"{user['height']:.1f} {height_unit}")
    table.add_row(":weight_lifter: Weight", f"{user['weight']:.1f} {weight_unit}")
    table.add_row(":footprints: Average Daily Steps", str(user["averageDailySteps"]))
    table.add_row(":calendar: Member Since", user["memberSince"])
    table.add_row(":clock1: Time Zone", user["timezone"])

    CONSOLE.print(table)


def display_sleep(sleep_data):
    """Sleep data formatter"""

    table = Table(title="Sleep Data Summary :sleeping:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Deep Sleep :bed:")
    table.add_column("Light Sleep :zzz:")
    table.add_column("REM Sleep :crescent_moon:")
    table.add_column("Wake Time :alarm_clock:")
    table.add_column("Efficiency :100:")

    for sleep in sleep_data["sleep"]:
        table.add_row(
            sleep["dateOfSleep"],
            f"{sleep['levels']['summary'].get('deep', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('light', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('rem', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('wake', {}).get('minutes', 'N/A')} min",
            f"{sleep['efficiency']}%",
        )

    CONSOLE.print(table)


def display_spo2(spo2_data):
    """SpO2 data formatter"""

    table = Table(title="SpO2 Data Summary :heart:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Minimum :red_circle:")
    table.add_column("Average :blue_circle:")
    table.add_column("Maximum :green_circle:")

    if isinstance(spo2_data, dict):
        spo2_data = [spo2_data]

    for spo2 in spo2_data:
        table.add_row(
            spo2.get("dateTime", "N/A"),
            str(spo2.get("value", {}).get("min", "N/A")),
            str(spo2.get("value", {}).get("avg", "N/A")),
            str(spo2.get("value", {}).get("max", "N/A")),
        )

    CONSOLE.print(table)


def display_heart_data(heart_data):
    """Heart data formatter"""

    table = Table(title="Heart Rate Time Series :heart:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Resting Heart Rate :heartpulse:")
    table.add_column("Heart Rate Zones :dart:")

    for activity in heart_data.get("activities-heart", []):
        date = activity.get("dateTime", "N/A")
        value = activity.get("value", {})
        resting_heart_rate = value.get("restingHeartRate", "N/A")

        zones_table = Table(show_header=True, header_style="bold magenta")
        zones_table.add_column("Zone :dart:")
        zones_table.add_column("Min :arrow_down:")
        zones_table.add_column("Max :arrow_up:")
        zones_table.add_column("Minutes :hourglass:")
        zones_table.add_column("Calories Out :fire:")

        for zone in value.get("heartRateZones", []):
            zones_table.add_row(
                zone.get("name", "N/A"),
                str(zone.get("min", "N/A")),
                str(zone.get("max", "N/A")),
                str(zone.get("minutes", "N/A")),
                (
                    f"{zone.get('caloriesOut', 'N/A'):.2f}"
                    if isinstance(zone.get("caloriesOut"), (int, float))
                    else "N/A"
                ),
            )

        table.add_row(date, str(resting_heart_rate), zones_table)

    CONSOLE.print(table)


def display_azm_time_series(azm_data):
    """AZM Time Series data formatter"""

    table = Table(title="AZM Time Series :runner:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Active Zone Minutes :stopwatch:")
    table.add_column("Fat Burn :fire:")
    table.add_column("Cardio :heart:")
    table.add_column("Peak :mountain:")

    for activity in azm_data.get("activities-active-zone-minutes", []):
        date = activity.get("dateTime", "N/A")
        value = activity.get("value", {})
        table.add_row(
            date,
            str(value.get("activeZoneMinutes", "N/A")),
            str(value.get("fatBurnActiveZoneMinutes", "N/A")),
            str(value.get("cardioActiveZoneMinutes", "N/A")),
            str(value.get("peakActiveZoneMinutes", "N/A")),
        )

    CONSOLE.print(table)


def display_breathing_rate(breathing_rate_data):
    """Breathing Rate data formatter"""

    table = Table(title="Breathing Rate Summary 🫁", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Breaths Per Minute :dash:")

    for br in breathing_rate_data.get("br", []):
        table.add_row(
            br.get("dateTime", "N/A"),
            str(br.get("value", {}).get("breathingRate", "N/A")),
        )

    CONSOLE.print(table)
