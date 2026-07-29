# -*- coding: utf-8 -*-
"""
Fitbit API
"""

import datetime

import requests

from .exceptions import FitbitAPIError
from .fitbit_setup import update_fitbit_token


class FitbitAPI:
    """Fitbit API"""

    TOKEN_API = "https://api.fitbit.com/oauth2/token"

    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.headers = self._create_headers()

    def _create_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def refresh_access_token(self):
        """Refresh token"""

        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }
        headers = {
            "Authorization": f"Basic {self.client_secret}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            FitbitAPI.TOKEN_API, data=payload, headers=headers, timeout=5
        )

        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens.get("access_token")
            self.refresh_token = tokens.get("refresh_token")
            self.headers = self._create_headers()
            update_fitbit_token(self.access_token, self.refresh_token)
        else:
            raise FitbitAPIError(f"Failed to refresh access token: {response.json()}")

    def make_request(self, method, url, **kwargs):
        """Make an API request and handle token refresh if needed."""

        try:
            response = requests.request(
                method, url, headers=self.headers, timeout=5, **kwargs
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                self.refresh_access_token()
                response = requests.request(
                    method, url, headers=self.headers, timeout=5, **kwargs
                )
                response.raise_for_status()
            else:
                raise FitbitAPIError(f"HTTP error occurred: {response.json()}") from e

        return response

    def get_user_profile(self):
        """Get Profile"""

        url = "https://api.fitbit.com/1/user/-/profile.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_devices(self):
        """Get Devices"""

        url = "https://api.fitbit.com/1/user/-/devices.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_sleep_log(self, start_date, end_date=None):
        """Get Sleep Logs by Date Range and Date"""

        date_range = f"{start_date}/{end_date}" if end_date else start_date
        url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{date_range}.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_heart_rate_time_series(self, start_date, end_date=None):
        """Get Heart Rate Time Series by Date Range and Date"""

        date_range = f"{start_date}/{end_date}" if end_date else f"{start_date}/1d"
        url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{date_range}.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_spo2_summary(self, start_date, end_date=None):
        """Get SpO2 Summary by Interval and Date"""

        date_range = f"{start_date}/{end_date}" if end_date else start_date
        url = f"https://api.fitbit.com/1/user/-/spo2/date/{date_range}.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_spo2_intraday(self, start_date, end_date=None):
        """Get SpO2 Intraday by Interval and Date"""

        date_range = f"{start_date}/{end_date}" if end_date else start_date
        url = f"https://api.fitbit.com/1/user/-/spo2/date/{date_range}/all.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_azm_time_series(self, start_date, end_date=None):
        """Get AZM Time Series by Interval and Data"""

        date_range = f"{start_date}/{end_date}" if end_date else f"{start_date}/1d"
        url = f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{date_range}.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_azm_intraday(self, start_date, end_date=None):
        """Get AZM Intraday by Interval and Data"""

        date_range = f"{start_date}/{end_date}" if end_date else f"{start_date}/1d"
        url = f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{date_range}/1min.json"
        response = self.make_request("GET", url)
        return response.json()

    def _fetch_chunked_data(self, url_template, key, start_date, end_date=None):
        """Fetch data in chunks <= 30 days if date range > 30 days."""
        if not end_date:
            url = url_template.format(date_range=start_date)
            return self.make_request("GET", url).json()

        start = (
            datetime.date.fromisoformat(start_date)
            if isinstance(start_date, str)
            else start_date
        )
        end = (
            datetime.date.fromisoformat(end_date)
            if isinstance(end_date, str)
            else end_date
        )
        if (end - start).days <= 30:
            url = url_template.format(date_range=f"{start_date}/{end_date}")
            return self.make_request("GET", url).json()

        aggregated = []
        curr_start = start
        result_dict = {}
        while curr_start <= end:
            curr_end = min(curr_start + datetime.timedelta(days=30), end)
            url = url_template.format(
                date_range=f"{curr_start.isoformat()}/{curr_end.isoformat()}"
            )
            res = self.make_request("GET", url).json()
            if not result_dict and isinstance(res, dict):
                result_dict = res.copy()
            if key in res and isinstance(res[key], list):
                aggregated.extend(res[key])
            curr_start = curr_end + datetime.timedelta(days=1)

        result_dict[key] = aggregated
        return result_dict

    def get_breathing_rate_summary(self, start_date, end_date=None):
        """Get Breathing Rate Summary by Interval and Data"""
        url_template = "https://api.fitbit.com/1/user/-/br/date/{date_range}.json"
        return self._fetch_chunked_data(url_template, "br", start_date, end_date)

    def get_breathing_rate_intraday(self, start_date, end_date=None):
        """Get Breathing Rate Intraday by Interval and Data"""
        url_template = "https://api.fitbit.com/1/user/-/br/date/{date_range}/all.json"
        return self._fetch_chunked_data(url_template, "br", start_date, end_date)

    def get_hrv_summary(self, start_date, end_date=None):
        """Get HRV Summary by Interval and Date"""
        url_template = "https://api.fitbit.com/1/user/-/hrv/date/{date_range}.json"
        return self._fetch_chunked_data(url_template, "hrv", start_date, end_date)

    def get_body_time_series(self, resource_path, start_date, end_date=None):
        """Get Body Time Series by Interval and Date"""

        date_range = f"{start_date}/{end_date}" if end_date else f"{start_date}/1d"
        url = f"https://api.fitbit.com/1/user/-/body/{resource_path}/date/{date_range}.json"
        response = self.make_request("GET", url)
        return response.json()

    def get_daily_activity_summary(self, start_date):
        """Get Daily Activity Summary"""

        url = f"https://api.fitbit.com/1/user/-/activities/date/{start_date}.json"
        response = self.make_request("GET", url)
        return response.json()
