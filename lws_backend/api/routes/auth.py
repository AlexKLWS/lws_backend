from fastapi import APIRouter, Depends

from lws_backend.api.dependencies.authorization import check_user_auth

router = APIRouter()


@router.get("/user-access")
async def user_access(user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception

    return user_auth[0]
