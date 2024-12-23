# -*- coding: utf-8 -*-
"""
Exceptions for Fitbit CLI
"""


class FitbitInitError(Exception):
    """Custom exception for Fitbit initial setup"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FitbitAPIError(Exception):
    """Custom exception for Fitbit API"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
