import uuid  # TODO: Add uuid.uuid4 as a request identifier

import pydantic
from fastapi import APIRouter, Depends, HTTPException, Path

from utils import logs

SUBDOMAIN_VALIDATION_REGEX = r"[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?"

# class KeyCloakServerCredentials(pydantic.BaseModel):
#     username: str
#     password: str


# async def common_parameters(creds: KeyCloakServerCredentials):
#     return creds


realm_router: APIRouter = APIRouter(
    prefix="/realms",
    tags=["realms"],
    # dependencies=[Depends(common_parameters)],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Invalid input"},
    },
)


@realm_router.get("/")
def read_realms():
    # TODO: Implement
    raise HTTPException(status_code=404, detail="Not implemented")


@realm_router.get("/{realm_name}")
async def get_realm(realm_name: str):
    # TODO: Implement
    raise HTTPException(status_code=404, detail="Not implemented")


@realm_router.post("/{realm_name}")
async def create_realm(
    realm_name: str = Path(
        min_length=1, max_length=64, regex=SUBDOMAIN_VALIDATION_REGEX
    )
):
    logs.logger.info("ABC", realm_name=realm_name)

    return {"message": "abc"}
