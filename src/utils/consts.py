import os

APP_NAME = os.environ.get("APP_NAME", "legit-py")
APP_VERSION = os.environ.get("APP_VERSION", "0.1.0")
APP_PORT: int = int(os.environ.get("APP_PORT", 8000))
APP_BIND_ADDR = os.environ.get("APP_BIND_ADDR", "0.0.0.0")

KC_PROTOCOL = os.environ.get("KC_PROTOCOL", "http")
KC_ADDRESS = os.environ.get("KC_ADDRESS", "keycloak")
KC_PORT = os.environ.get("KC_PORT", 8080)
KC_URL_PREFIX = f"{KC_PROTOCOL}://{KC_ADDRESS}:{KC_PORT}"
KC_REALMS_ROUTE = "auth/realms"
KC_DEFAULT_REALM = "master"
KC_AUTH_ENDPOINT = "protocol/openid-connect/token"
