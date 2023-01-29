from pydantic import BaseSettings, Field, AnyHttpUrl, SecretStr
from ipaddress import IPv4Address


class Settings(BaseSettings):
    name: str = Field(default="legit-py", env="APP_NAME")
    version: str = Field(default="0.1.0", env="APP_VERSION")
    port: int = Field(ge=1024, lt=65535, default=8000, env="APP_PORT")
    address: IPv4Address = Field(default="0.0.0.0", env="APP_BIND_ADDR")
    keycloak_admin_username: str = Field(default="admin", env="KEYCLOAK_USER")
    keycloak_admin_password: SecretStr = Field(default="", env="KEYCLOAK_PASSWORD")

    keycloak_address: AnyHttpUrl = Field(
        env="KC_ADDRESS", default="http://keycloak:8080"
    )
    keycloak_realms_route: str = "auth/realms"
    keycloak_default_realm: str = "master"
    keycloak_auth_endpoint: str = "protocol/openid-connect/token"
