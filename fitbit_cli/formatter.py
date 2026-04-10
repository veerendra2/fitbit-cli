# -*- coding: utf-8 -*-
"""
Json Data Formatter
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text

CONSOLE = Console()


def display_user_profile(user_data, as_json=False):
    """User data formatter"""

    user = user_data["user"]
    height_unit = "cm" if user["heightUnit"] == "METRIC" else "in"
    weight_unit = "kg"
    if user["weightUnit"] == "UK":
        weight_unit = "stone"
    elif user["weightUnit"] == "US":
        weight_unit = "pounds"

    if as_json:
        return {
            "user_profile": {
                "first_name": user["firstName"],
                "last_name": user["lastName"],
                "date_of_birth": user["dateOfBirth"],
                "age": user["age"],
                "gender": user["gender"],
                "height": f"{user['height']:.1f} {height_unit}",
                "weight": f"{user['weight']:.1f} {weight_unit}",
                "average_daily_steps": user["averageDailySteps"],
                "member_since": user["memberSince"],
                "timezone": user["timezone"],
            }
        }

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
    return None


def display_sleep(sleep_data, as_json=False):
    """Sleep data formatter"""

    if as_json:
        return {
            "sleep": [
                {
                    "date": s["dateOfSleep"],
                    "deep_minutes": s["levels"]["summary"]
                    .get("deep", {})
                    .get("minutes"),
                    "light_minutes": s["levels"]["summary"]
                    .get("light", {})
                    .get("minutes"),
                    "rem_minutes": s["levels"]["summary"].get("rem", {}).get("minutes"),
                    "wake_minutes": s["levels"]["summary"]
                    .get("wake", {})
                    .get("minutes"),
                    "efficiency": s["efficiency"],
                    "time_in_bed_hours": round(s["timeInBed"] / 60, 1),
                }
                for s in sleep_data["sleep"]
            ]
        }

    table = Table(title="Sleep Data Summary :sleeping:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Deep Sleep :bed:")
    table.add_column("Light Sleep :zzz:")
    table.add_column("REM Sleep :crescent_moon:")
    table.add_column("Wake Time :alarm_clock:")
    table.add_column("Efficiency :100:")
    table.add_column("Time in Bed :clock1:")

    for sleep in sleep_data["sleep"]:
        table.add_row(
            sleep["dateOfSleep"],
            f"{sleep['levels']['summary'].get('deep', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('light', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('rem', {}).get('minutes', 'N/A')} min",
            f"{sleep['levels']['summary'].get('wake', {}).get('minutes', 'N/A')} min",
            f"{sleep['efficiency']}%",
            f"{sleep['timeInBed'] / 60:.1f} hr",
        )

    CONSOLE.print(table)
    return None


def display_spo2(spo2_data, as_json=False):
    """SpO2 data formatter"""

    if isinstance(spo2_data, dict):
        spo2_data = [spo2_data]

    if as_json:
        return {
            "spo2": [
                {
                    "date": s.get("dateTime"),
                    "min": s.get("value", {}).get("min"),
                    "avg": s.get("value", {}).get("avg"),
                    "max": s.get("value", {}).get("max"),
                }
                for s in spo2_data
            ]
        }

    table = Table(title="SpO2 Data Summary :heart:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Minimum :red_circle:")
    table.add_column("Average :blue_circle:")
    table.add_column("Maximum :green_circle:")

    for spo2 in spo2_data:
        table.add_row(
            spo2.get("dateTime", "N/A"),
            str(spo2.get("value", {}).get("min", "N/A")),
            str(spo2.get("value", {}).get("avg", "N/A")),
            str(spo2.get("value", {}).get("max", "N/A")),
        )

    CONSOLE.print(table)
    return None


def display_heart_data(heart_data, as_json=False):
    """Heart data formatter"""

    if as_json:
        return {
            "heart": [
                {
                    "date": a.get("dateTime"),
                    "resting_heart_rate": a.get("value", {}).get("restingHeartRate"),
                    "zones": [
                        {
                            "name": z.get("name"),
                            "min": z.get("min"),
                            "max": z.get("max"),
                            "minutes": z.get("minutes"),
                            "calories_out": (
                                round(z["caloriesOut"], 2)
                                if isinstance(z.get("caloriesOut"), (int, float))
                                else None
                            ),
                        }
                        for z in a.get("value", {}).get("heartRateZones", [])
                    ],
                }
                for a in heart_data.get("activities-heart", [])
            ]
        }

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
        zones_table.add_column("Calories Out (kcal) :fire:")

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
    return None


def display_azm_time_series(azm_data, as_json=False):
    """AZM Time Series data formatter"""

    if as_json:
        return {
            "active_zone": [
                {
                    "date": a.get("dateTime"),
                    "active_zone_minutes": a.get("value", {}).get("activeZoneMinutes"),
                    "fat_burn_minutes": a.get("value", {}).get(
                        "fatBurnActiveZoneMinutes"
                    ),
                    "cardio_minutes": a.get("value", {}).get("cardioActiveZoneMinutes"),
                    "peak_minutes": a.get("value", {}).get("peakActiveZoneMinutes"),
                }
                for a in azm_data.get("activities-active-zone-minutes", [])
            ]
        }

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
    return None


def display_breathing_rate(breathing_rate_data, as_json=False):
    """Breathing Rate data formatter"""

    if as_json:
        return {
            "breathing_rate": [
                {
                    "date": br.get("dateTime"),
                    "breathing_rate": br.get("value", {}).get("breathingRate"),
                }
                for br in breathing_rate_data.get("br", [])
            ]
        }

    table = Table(title="Breathing Rate Summary 🫁", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Breaths Per Minute :dash:")

    for br in breathing_rate_data.get("br", []):
        table.add_row(
            br.get("dateTime", "N/A"),
            str(br.get("value", {}).get("breathingRate", "N/A")),
        )

    CONSOLE.print(table)
    return None


def display_hrv(hrv_data, as_json=False):
    """HRV data formatter"""

    if as_json:
        return {
            "hrv": [
                {
                    "date": h.get("dateTime"),
                    "daily_rmssd": h.get("value", {}).get("dailyRmssd"),
                    "deep_rmssd": h.get("value", {}).get("deepRmssd"),
                }
                for h in hrv_data.get("hrv", [])
            ]
        }

    table = Table(title="HRV Data Summary :heartpulse:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Daily RMSSD :chart_with_upwards_trend:")
    table.add_column("Deep RMSSD :sleeping:")

    for hrv in hrv_data.get("hrv", []):
        table.add_row(
            hrv.get("dateTime", "N/A"),
            str(hrv.get("value", {}).get("dailyRmssd", "N/A")),
            str(hrv.get("value", {}).get("deepRmssd", "N/A")),
        )

    CONSOLE.print(table)
    return None


def display_weight(weight_data, as_json=False):
    """Weight data formatter"""

    if as_json:
        return {
            "weight": [
                {
                    "date": weight.get("date"),
                    "time": weight.get("time"),
                    "weight": weight.get("weight"),
                    "bmi": weight.get("bmi"),
                }
                for weight in weight_data.get("weight", [])
            ]
        }

    table = Table(title="Weight Log :balance_scale:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Time :clock3:")
    table.add_column("Weight :weight_lifter:")
    table.add_column("BMI :straight_ruler:")

    for weight in weight_data.get("weight", []):
        table.add_row(
            str(weight.get("date", "N/A")),
            str(weight.get("time", "N/A")),
            str(weight.get("weight", "N/A")),
            str(weight.get("bmi", "N/A")),
        )

    CONSOLE.print(table)
    return None


def display_body_fat(body_fat_data, as_json=False):
    """Body fat data formatter"""

    if as_json:
        return {
            "body_fat": [
                {
                    "date": body_fat.get("date"),
                    "time": body_fat.get("time"),
                    "fat": body_fat.get("fat"),
                }
                for body_fat in body_fat_data.get("fat", [])
            ]
        }

    table = Table(title="Body Fat Log :anatomical_heart:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Time :clock3:")
    table.add_column("Body Fat % :chart_with_upwards_trend:")

    for body_fat in body_fat_data.get("fat", []):
        table.add_row(
            str(body_fat.get("date", "N/A")),
            str(body_fat.get("time", "N/A")),
            str(body_fat.get("fat", "N/A")),
        )

    CONSOLE.print(table)
    return None


def display_devices(devices, as_json=False):
    """Devices list formatter"""

    def format_mac(mac):
        if mac == "N/A" or len(mac) % 2:
            return mac
        return ":".join(mac[i : i + 2] for i in range(0, len(mac), 2))

    if as_json:
        return {
            "devices": [
                {
                    "battery_level": device.get("batteryLevel"),
                    "device": device.get("deviceVersion"),
                    "type": device.get("type"),
                    "last_sync_time": device.get("lastSyncTime"),
                    "mac_address": format_mac(str(device.get("mac", "N/A"))),
                }
                for device in devices
            ]
        }

    table = Table(title="Devices List :link:", show_header=True)

    table.add_column("Battery % :battery:")
    table.add_column("Device :watch:")
    table.add_column("Type :iphone:")
    table.add_column("Last Sync Time :clock3:")
    table.add_column("MAC Address :label:")

    for device in devices:
        mac_address = format_mac(str(device.get("mac", "N/A")))
        table.add_row(
            f"{str(device.get('batteryLevel', 'N/A'))}%",
            str(device.get("deviceVersion", "N/A")),
            str(device.get("type", "N/A")),
            str(device.get("lastSyncTime", "N/A")),
            mac_address,
        )

    CONSOLE.print(table)
    return None


def display_activity(activity_data, unit_system, as_json=False):
    """Activity data formatter"""

    dis_unit = "km" if unit_system != "US" else "miles"

    if as_json:
        return {
            "activities": [
                {
                    "date": day.get("date"),
                    "activities": [
                        {
                            "start_time": a.get("startTime"),
                            "name": a.get("name"),
                            "description": a.get("description"),
                            "distance": (
                                f"{a.get('distance', 'N/A')} {dis_unit}"
                                if a.get("distance") is not None
                                else None
                            ),
                            "steps": a.get("steps"),
                            "calories": a.get("calories"),
                            "duration_minutes": round(a.get("duration", 0) / 60000, 1),
                        }
                        for a in day.get("activities", [])
                    ],
                }
                for day in activity_data
            ]
        }

    table = Table(title="Daily Activities :runner:", show_header=True)

    table.add_column("Date :calendar:")
    table.add_column("Activities :clipboard:")

    for activity_day in activity_data:
        activity_table = Table(show_header=True, header_style="bold magenta")
        activity_table.add_column("Start Time :alarm_clock:")
        activity_table.add_column("Name :running_shirt_with_sash:")
        activity_table.add_column("Description :memo:", width=30)
        activity_table.add_column("Distance :straight_ruler:")
        activity_table.add_column("Steps :footprints:")
        activity_table.add_column("Calories (kcal) :fire:")
        activity_table.add_column("Duration :hourglass:")

        for activity in activity_day.get("activities", []):
            duration_min = activity.get("duration", 0) / 60000
            activity_table.add_row(
                activity.get("startTime", ""),
                activity.get("name", "N/A"),
                Text(activity.get("description", "N/A"), overflow="fold"),
                f"{activity.get('distance', 'N/A')} {dis_unit}",
                str(activity.get("steps", "N/A")),
                str(activity.get("calories", "N/A")),
                f"{duration_min:.1f} min",
            )
        table.add_row(activity_day.get("date", ""), activity_table)

    CONSOLE.print(table)
    return None
