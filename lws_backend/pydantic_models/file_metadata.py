from typing import Optional, List
from pydantic import BaseModel


class FileMetadata(BaseModel):
    id: str
    referenceId: Optional[str] = None
    newName: Optional[str] = None
    folder: Optional[str] = None


class FileMetadataPostRequest(BaseModel):
    metaData: List[FileMetadata]
