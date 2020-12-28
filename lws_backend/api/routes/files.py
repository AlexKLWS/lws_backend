import os
import uuid
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status, Depends

from lws_backend.files import add_file_metadata, pop_file_metadata
from lws_backend.api.dependencies.authorization import check_user_auth
from lws_backend.pydantic_models.user_access_rights import UserAccessRights
from lws_backend.pydantic_models.file_metadata import FileMetadataPostRequest
from lws_backend.core.config import (
    ASSETS_PATH,
)

router = APIRouter()


@router.put("/metadata")
async def add_metadata(metadataRequest: FileMetadataPostRequest, user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception
    access_rights = user_auth[0]
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    for metadata in metadataRequest.metaData:
        metadata.referenceId = str(uuid.uuid4())
    add_file_metadata(metadataRequest)
    return metadataRequest


@router.put("")
async def add_files(referenceId: str = Form(...), file: UploadFile = File(...),
                    user_auth=Depends(check_user_auth)):
    exception = user_auth[1]
    if exception:
        raise exception
    access_rights = user_auth[0]
    if access_rights != UserAccessRights.WRITE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required access rights")

    file_metadata = pop_file_metadata(referenceId)
    dir = ASSETS_PATH
    if file_metadata.folder:
        dir = os.path.join(dir, file_metadata.folder)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
            os.chmod(dir, 0o755)

    file_format = file.filename.split(".")[-1]
    file_name = file_metadata.newName + "." + file_format if file_metadata.newName else file.filename

    file_path = os.path.join(dir, file_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
    os.chmod(file_path, 0o644)

    return file_path
