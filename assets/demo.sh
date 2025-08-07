#!/usr/bin/env bash

# To record demo, run
# asciinema rec my-demo.cast --command "./demo.sh"

# To find and replace
# sed 's/banana/apple/g' fruits.txt


# To covert to gif
# go install github.com/asciinema-cli/agg@latest
# agg my-demo.cast my-demo.gif

# To upload
# asciinema auth
# asciinema upload demo.cast

# Typing speed (delay between characters)
speed=0.01

# Pause between commands (in seconds)
pause=1

# Function to "type" a string
type_text() {
  text="$1"
  for ((i=0; i<${#text}; i++)); do
    echo -n "${text:$i:1}"
    sleep $speed
  done
  echo
}

# Function to type a comment and run a command on a new line
type_text_and_run() {
  comment="$1"
  command="$2"
  type_text "$comment"
  echo "$command"
  eval "$command"
  sleep $pause
}

clear

# --- Start of the demo script ---

# Welcome
type_text "# Welcome to the fitbit-cli demo! Let's see the available commands."
sleep 1
fitbit-cli -h
sleep 1

# Sleep data section
echo
type_text_and_run "# Get today's sleep data." "fitbit-cli --sleep"

# Relative date range
echo
type_text_and_run "# Get sleep data for the last 3 days." "fitbit-cli -s last-3-days"

echo
type_text_and_run "# Or for the last week." "fitbit-cli -s last-week"

# Specific date range
echo
type_text_and_run "# Fetch sleep data for a specific date range." "fitbit-cli -s 2025-04-12,2025-04-20"

# Specific single date
echo
type_text_and_run "# Or just a single date." "fitbit-cli -s 2025-04-21"

# Other APIs section
echo
type_text "# Now for a few other APIs. Note that they all support the same date and relative date queries we just used."
sleep 1

# SpO2
echo
type_text_and_run "# Get your SpO2 data." "fitbit-cli -o"

# Breathing Rate
echo
type_text_and_run "# Get your breathing rate summary." "fitbit-cli -b"

# Active zone
echo
type_text_and_run "# Get your active zone minutes." "fitbit-cli -a yesterday"

# Profile
echo
type_text_and_run "# Also get your profile data with the same flag." "fitbit-cli -u"

# Devices
echo
type_text_and_run "# Finally, see your connected devices." "fitbit-cli -d"

# End message
echo
type_text "# Thanks for watching!"
sleep 1