# -*- coding: utf-8 -*-
"""
Main Module
"""

from . import fitbit_setup as setup
from . import output
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

    if args.raw_json:
        output.raw_json_display(fitbit, args)
    elif args.json:
        output.json_display(fitbit, args)
    else:
        output.table_display(fitbit, args)
