import json
import os
from typing import Dict

import requests
from pydantic import SecretStr

from utils import logs
from utils.consts import (
    APP_NAME,
    APP_VERSION,
    KC_AUTH_ENDPOINT,
    KC_DEFAULT_REALM,
    KC_REALMS_ROUTE,
    KC_URL_PREFIX,
)


def get_access_token(response: requests.Response) -> SecretStr:
    try:
        return SecretStr(response.json()["access_token"])
    except KeyError:
        logs.logger.exception(
            "Authorization was not successful", response=response.json()
        )
        raise SystemExit(1)


def auth_admin(realm: str = KC_DEFAULT_REALM) -> requests.Response:
    admin_username: str = os.environ.get("KEYCLOAK_USER", "admin")
    _admin_password: SecretStr = SecretStr(os.environ.get("KEYCLOAK_PASSWORD", ""))
    if len(_admin_password) == 0:
        raise ValueError(
            "No password for the admin account has been received, please use 'KEYCLOAK_PASSWORD'"
        )
    return auth_user(admin_username, _admin_password, realm)


def auth_user(
    username: str, _password: SecretStr, realm: str = KC_DEFAULT_REALM
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
        "password": _password.get_secret_value(),
    }
    logs.logger.debug("Authenticating new user!", user=username)
    return requests.post(auth_endpoint, headers=headers, data=credentials)


def add_realm(_token: SecretStr, realm: str) -> requests.Response:
    add_realm_endpoint: str = f"{KC_URL_PREFIX}/auth/admin/realms"
    headers = {
        "user-agent": f"{APP_NAME}/{APP_VERSION}",
        "Content-type": "application/json",
        "Authorization": f"bearer {_token.get_secret_value()}",
    }

    realm_props = {
        "id": realm,
        "realm": realm,
    }

    return requests.post(
        add_realm_endpoint, headers=headers, data=json.dumps(realm_props)
    )
