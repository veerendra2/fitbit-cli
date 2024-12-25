# -*- coding: utf-8 -*-
"""
Fitbit initial setup
"""

import getpass
import json
import secrets
import string
import threading
import webbrowser
from base64 import b64encode, urlsafe_b64encode
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from rich.prompt import Prompt

from .exceptions import FitbitInitError
from .formatter import CONSOLE

BASE_URL = "https://www.fitbit.com/oauth2/authorize"
FITBIT_TOKEN_PATH = f"{Path.home()}/.fitbit/token.json"
SCOPE = [
    "activity",
    "cardio_fitness",
    "electrocardiogram",
    "heartrate",
    "irregular_rhythm_notifications",
    "location",
    "nutrition",
    "oxygen_saturation",
    "profile",
    "respiratory_rate",
    "settings",
    "sleep",
    "social",
    "temperature",
    "weight",
]
TOKEN_URL = "https://api.fitbit.com/oauth2/token"


class RequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler"""

    code = None

    def do_GET(self):  # pylint: disable=C0103
        """Handle GET request"""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        RequestHandler.code = query_params.get("code", [""])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"You can close this window now")

        threading.Thread(target=self.server.shutdown).start()


def start_server():
    """Start simple HTTP server to catch token"""

    with HTTPServer(("127.0.0.1", 8080), RequestHandler) as httpd:
        CONSOLE.print(":computer: Serving on http://127.0.0.1:8080")
        httpd.serve_forever()
    return RequestHandler.code


def fitbit_init_setup():
    """Fitbit initial setup"""

    # --------- Generate code challenge using random strings ---------
    code_verifier = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(128)
    )
    code_challenge = (
        urlsafe_b64encode(sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )

    # --------- Get client ID and constructs authorization URL ---------
    client_id = Prompt.ask(":bust_in_silhouette: Enter your Client ID")
    assert client_id, "Invalid Client ID"

    authorization_url = (
        f"{BASE_URL}?client_id={client_id}&response_type=code"
        f"&code_challenge={code_challenge}&code_challenge_method=S256"
        f"&scope={'+'.join(SCOPE)}"
    )

    # --------- Get authorization code ---------
    CONSOLE.print(
        f":earth_asia: Opening below URL in browser to authorize the app \n\n{authorization_url}\n"
    )
    try:
        browser_status = webbrowser.open(authorization_url)
        if browser_status:
            CONSOLE.print(
                ":satellite: Waiting for authorization... "
                + "(Check your browser or press 'Ctrl+C', authorize the app by opening the"
                + " above URL in your browser and past the redirect URL manually.)\n"
            )
            authorization_code = start_server()
        else:
            raise FitbitInitError("Failed to open the URL in browser")
    except (KeyboardInterrupt, FitbitInitError):
        CONSOLE.print("\n:unamused: Error while opening the URL...")
        CONSOLE.print(
            ":neutral_face: Authrize the app by opening the above URL in your"
            + "browser and past the redirect URL"
        )
        redirect_url = Prompt.ask(":clipboard: Paste the redirect URL: ")
        assert redirect_url, "Invalid URL"

        authorization_code = parse_qs(urlparse(redirect_url).query).get("code", [None])[
            0
        ]

    # --------- Get access and refresh tokens ---------
    client_secret = getpass.getpass("\n🔑 Enter your Client Secret: ")
    assert client_secret, "Invalid Client Secret"

    encoded_auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "code_verifier": code_verifier,
        },
        timeout=5,
    )

    if response.status_code == 200:
        response_json = response.json()
        Path(FITBIT_TOKEN_PATH).parent.mkdir(parents=True, exist_ok=True)
        token_content = {
            "access_token": response_json.get("access_token", ""),
            "refresh_token": response_json.get("refresh_token", ""),
            "client_id": client_id,
            "secret": encoded_auth,
        }
        with open(FITBIT_TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump(token_content, f)

        CONSOLE.print(
            f":floppy_disk: Saving fitbit token in {FITBIT_TOKEN_PATH}",
            style="bold green",
        )
    else:
        CONSOLE.print(
            f":unamused: Failed to get tokens: {response.json()['errors'][0]['errorType']}",
            style="bold red",
        )


def read_fitbit_token():
    """Read Fitbit token from the file and return as a JSON object."""

    try:
        with open(FITBIT_TOKEN_PATH, "r", encoding="utf-8") as f:
            token_content = json.load(f)
    except FileNotFoundError as e:
        raise FitbitInitError(
            f"Token file not found at {FITBIT_TOKEN_PATH}. Please run the initialization with --init-auth"
        ) from e
    except json.JSONDecodeError:
        raise FitbitInitError(
            "Error decoding the token file. Please re-run the initialization with --init-auth"
        ) from e

    return token_content


def write_fitbit_token(token_content):
    """Write Fitbit token to the file."""

    Path(FITBIT_TOKEN_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(FITBIT_TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(token_content, f)


def update_fitbit_token(access_token, refresh_token):
    """Update Fitbit token in the file."""

    token_content = read_fitbit_token()
    token_content["access_token"] = access_token
    token_content["refresh_token"] = refresh_token
    write_fitbit_token(token_content)
