import fastapi
from typing import Dict
from fastapi import APIRouter, HTTPException, Path

from utils import client, logs
from utils.settings import Settings

SUBDOMAIN_VALIDATION_REGEX = r"[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?"


realm_router: APIRouter = APIRouter(
    prefix="/realms",
    tags=["realms"],
    responses={
        201: {"description": "Success"},
        401: {"description": "Unauthorized"},
        409: {"description": "Conflict"},
        404: {"description": "Not found"},
        422: {"description": "Invalid input"},
    },
)


@realm_router.get("/")
def read_realms():
    raise HTTPException(status_code=404, detail="Not implemented")


@realm_router.get("/{realm_name}")
async def get_realm(realm_name: str):
    raise HTTPException(status_code=404, detail="Not implemented")


def create_realm_retry(
    request: fastapi.Request, realm_name: str, retries: int = 1
) -> Dict[str, str]:
    app_state = request.app.state
    _token = app_state.access_token
    settings: Settings = app_state.settings
    res = client.add_realm(settings, _token, realm_name)
    if res.status_code == 201:
        # The realm was successfully created!
        logs.logger.info("New Realm has been created!", realm_name=realm_name)
        return {"message": f"Created realm '{realm_name}'"}
    if res.status_code == 401 and retries:
        # Token is invalid, reauthenticating
        logs.logger.info("Invalid token, reauthenticating", retries=retries)
        res = client.auth_user(settings)
        app_state.access_token = client.get_access_token(res)
        return create_realm_retry(request, realm_name, retries - 1)
    if res.status_code == 409:
        # The realm exists in the system.
        logs.logger.warning("The realm already exists in the system", realm=realm_name)
        return {"message": f"Realm '{realm_name}' already exists in the system."}
    raise HTTPException(status_code=res.status_code, detail="Could not create realm")


@realm_router.post("/{realm_name}")
async def create_realm(
    request: fastapi.Request,
    realm_name: str = Path(
        min_length=1, max_length=64, regex=SUBDOMAIN_VALIDATION_REGEX
    ),
):
    return create_realm_retry(request, realm_name)
