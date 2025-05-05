# Fitbit CLI

[![Release](https://github.com/veerendra2/fitbit-cli/actions/workflows/release.yml/badge.svg)](https://github.com/veerendra2/fitbit-cli/actions/workflows/release.yml) [![PyPI - Status](https://img.shields.io/pypi/status/fitbit-cli)
](https://pypi.org/project/fitbit-cli/) [![PyPI - Version](https://img.shields.io/pypi/v/fitbit-cli)
](https://pypi.org/project/fitbit-cli/)

> This is not an official Fitbit CLI

Access your Fitbit data directly from your terminal 💻. View 💤 sleep logs, ❤️ heart rate, 🏋️‍♂️ activity levels, 🩸 SpO2, and more, all presented in a simple, easy-to-read table format!

<p align="center">
  <img alt="Fitbit logo", width="250" src="https://raw.githubusercontent.com/veerendra2/fitbit-cli/refs/heads/main/assets/Fitbit_Logo_White_RGB.jpg">
</p>

[![asciicast](https://asciinema.org/a/696114.svg)](https://asciinema.org/a/696114)

## Supported Web APIs

> Only `GET` APIs are supported!

| API                                                                                                                     | Status |
| ----------------------------------------------------------------------------------------------------------------------- | ------ |
| [User](https://dev.fitbit.com/build/reference/web-api/user/)                                                            | ✅     |
| [Sleep](https://dev.fitbit.com/build/reference/web-api/sleep/)                                                          | ✅     |
| [SpO2](https://dev.fitbit.com/build/reference/web-api/spo2/)                                                            | ✅     |
| [Heart Rate Time Series](https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/)                          | ✅     |
| [Active Zone Minutes (AZM) Time Series](https://dev.fitbit.com/build/reference/web-api/active-zone-minutes-timeseries/) | ✅     |
| [Activity](https://dev.fitbit.com/build/reference/web-api/activity/)                                                    | ✅     |

## Usage Guide

1. Install the Fitbit CLI

```bash
python -m pip install fitbit-cli
```

2. See Help

```bash
fitbit-cli -h
usage: fitbit-cli [-h] [-i] [-s [DATE[,DATE]|RELATIVE]] [-o [DATE[,DATE]|RELATIVE]] [-e [DATE[,DATE]|RELATIVE]] [-a [DATE[,DATE]|RELATIVE]]
                  [-b [DATE[,DATE]|RELATIVE]] [-u] [-v]

Fitbit CLI -- Access your Fitbit data at your terminal.

options:
  -h, --help            show this help message and exit
  -i, --init-auth       Initialize Fitbit iterative authentication setup
  -v, --version         Show fitbit-cli version

APIs:
  Specify a date, date range (YYYY-MM-DD[,YYYY-MM-DD]), or relative date.
  Relative dates: yesterday, last-week, last-month, last-N-days/weeks/months (e.g., last-2-days).
  If not provided, defaults to today's date.

  -s, --sleep [DATE[,DATE]|RELATIVE]
                        Show sleep data
  -o, --spo2 [DATE[,DATE]|RELATIVE]
                        Show SpO2 data
  -e, --heart [DATE[,DATE]|RELATIVE]
                        Show Heart Rate Time Series data
  -a, --active-zone [DATE[,DATE]|RELATIVE]
                        Show Active Zone Minutes (AZM) Time Series data
  -b, --breathing-rate [DATE[,DATE]|RELATIVE]
                        Show Breathing Rate Summary data
  -u, --show-user-profile
                        Show user profile data
```

3. Register Fitbit App

   1. Go to [https://dev.fitbit.com/apps](https://dev.fitbit.com/apps)
   2. Click on "REGISTER AN APP" tab
   3. Follow below example and register an app

     <p align="left">
       <img alt="Fitbit logo", width="700" src="https://raw.githubusercontent.com/veerendra2/fitbit-cli/refs/heads/main/assets/fitbit-app-registration.png">
     </p>

4. Run the following command to set up interactive authentication and store the Fitbit token locally

   ```bash
    fitbit-cli --init-auth
   ```

   [![asciicast](https://asciinema.org/a/696115.svg)](https://asciinema.org/a/696115)

5. Start using it 😎

```bash
fitbit-cli -s
                                            Sleep Data Summary 😴
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Date 📆    ┃ Deep Sleep 🛏 ┃ Light Sleep 💤 ┃ REM Sleep 🌙 ┃ Wake Time ⏰ ┃ Efficiency 💯 ┃ Time in Bed 🕐 ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ 2025-05-03 │ 129 min      │ 271 min        │ 140 min      │ 66 min       │ 57%           │ 10.1 hr        │
└────────────┴──────────────┴────────────────┴──────────────┴──────────────┴───────────────┴────────────────┘
```

_**NOTE: The token is valid for only 8 hours, `fitbit-cli` automatically refreshes the token when it expires.**_

## Local Development

- [Fitbit Docs](https://dev.fitbit.com/build/reference/web-api/)
- [OAuth Tutorial](https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/)

```bash
git clone git@github.com:veerendra2/fitbit-cli.git
cd fitbit-cli

python -m venv venv
source venv/bin/activate
python -m pip install -e .

deactivate
```
