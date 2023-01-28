import json
import os
from typing import Dict

import requests

from utils import logs
from utils.consts import (APP_NAME, APP_VERSION, KC_AUTH_ENDPOINT,
                          KC_DEFAULT_REALM, KC_REALMS_ROUTE, KC_URL_PREFIX)


def create_superuser():
    """
    Create a maintenance user which the application will use in order to communicate with the KeyCloak server without overusing the admin account.
    """
    admin_username: str = os.environ.get("KEYCLOAK_USER", "admin")
    _admin_password: str | None = os.environ.get("KEYCLOAK_PASSWORD", None)
    maintenance_username: str = os.environ.get("KC_USER_NAME", "maintenance")
    _maintenance_password: str | None = os.environ.get("KC_USER_PASS", None)

    if not all((_admin_password, _maintenance_password)):
        logs.logger.exception(
            "Both 'KC_ADMIN_PASSWORD' and 'KC_USER_PASS' are required"
        )
        exit(1)

    try:
        auth_res = auth_user(admin_username, _admin_password)
        # If the basic user creation doesn't work, terminate the app
        auth_res.raise_for_status()
        _token = auth_res.json()["access_token"]
    except requests.HTTPError:
        logs.logger.exception(
            "Could not authenticate to KeyCloak. Terminating app...",
            url=KC_URL_PREFIX,
            user=admin_username,
        )
        exit(1)
    except KeyError:
        logs.logger.exception(
            "Could not fetch the token out of the authentication response. Terminating app..."
        )
        exit(1)
    except:
        logs.logger.exception("Exception has occured. Terminating app...")
        exit(1)

    try:
        create_user_res = create_user(
            _token, maintenance_username, _maintenance_password
        )
        create_user_res.raise_for_status()
    except requests.HTTPError:
        logs.logger.exception(
            "Could not create new user. Terminating...", user=maintenance_username
        )
        logs.logger.debug(create_user_res.json())
        exit(1)


def auth_user(
    username: str, _password: str, realm: str = KC_DEFAULT_REALM
) -> requests.Response:
    auth_endpoint: str = f"{KC_URL_PREFIX}/{KC_REALMS_ROUTE}/{realm}/{KC_AUTH_ENDPOINT}"
    headers = {
        "user-agent": f"{APP_NAME}/{APP_VERSION}",
        "Content-type": "application/x-www-form-urlencoded",
    }

    credentials: Dict[str, str] = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": username,
        "password": _password,
    }
    return requests.post(auth_endpoint, headers=headers, data=credentials)


def create_user(
    _token: str, new_username: str, _new_password: str, realm: str = KC_DEFAULT_REALM
) -> requests.Response:
    add_user_endpoint = f"{KC_URL_PREFIX}/auth/admin/realms/{realm}/users"
    user_rep = {
        "enabled": True,
        "username": new_username,
        "credentials": [
            {"type": "password", "value": _new_password, "temporary": False}
        ],
    }

    headers = {
        "user-agent": f"{APP_NAME}/{APP_VERSION}",
        "Content-type": "application/json",
        "Authorization": f"bearer {_token}",
    }
    return requests.post(add_user_endpoint, headers=headers, data=json.dumps(user_rep))
