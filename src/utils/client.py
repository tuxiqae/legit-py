import json
from typing import Dict

import requests
from pydantic import SecretStr

from utils import logs
from utils.settings import Settings


def get_access_token(response: requests.Response) -> SecretStr:
    try:
        return SecretStr(response.json()["access_token"])
    except KeyError:
        logs.logger.exception(
            "Authorization was not successful", response=response.json()
        )
        raise SystemExit(1)


# def auth_admin(settings: Settings, realm: str) -> requests.Response:
#     if len(settings) == 0:
#         raise ValueError(
#             "No password for the admin account has been received, please use 'KEYCLOAK_PASSWORD'"
#         )
#     return auth_user(admin_username, _admin_password, realm)


def auth_user(settings: Settings) -> requests.Response:
    realm = settings.keycloak_default_realm
    auth_endpoint: str = f"{settings.keycloak_address}/{settings.keycloak_realms_route}/{realm}/{settings.keycloak_auth_endpoint}"
    headers = {
        "user-agent": f"{settings.name}/{settings.version}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    if len(settings.keycloak_admin_password) == 0:
        raise ValueError(
            "No password for the admin account has been received, please set 'KEYCLOAK_PASSWORD'"
        )

    credentials: Dict[str, str] = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": settings.keycloak_admin_username,
        "password": settings.keycloak_admin_password.get_secret_value(),
    }
    logs.logger.debug("Authenticating new user!", user=settings.keycloak_admin_username)
    return requests.post(auth_endpoint, headers=headers, data=credentials)


def add_realm(settings: Settings, _token: SecretStr, realm: str) -> requests.Response:
    add_realm_endpoint: str = f"{settings.keycloak_address}/auth/admin/realms"
    headers = {
        "user-agent": f"{settings.name}/{settings.version}",
        "Content-type": "application/json",
        "Authorization": f"bearer {_token.get_secret_value()}",
    }

    realm_props = {"id": realm, "realm": realm, "enabled": True}

    return requests.post(
        add_realm_endpoint, headers=headers, data=json.dumps(realm_props)
    )
