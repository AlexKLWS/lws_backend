from typing import Dict
from threading import Lock
import uuid

from lws_backend.pydantic_models.file_metadata import FileMetadata, FileMetadataPostRequest

mutex = Lock()
file_metadata: Dict[str, FileMetadata] = {}


def add_file_metadata(metadataRequest: FileMetadataPostRequest):
    for metadata in metadataRequest.metaData:
        metadata.referenceId = str(uuid.uuid4())
    mutex.acquire()
    try:
        for metadata in metadataRequest.metaData:
            file_metadata[metadata.referenceId] = metadata
        return metadataRequest
    finally:
        mutex.release()


def pop_file_metadata(reference_id: str):
    mutex.acquire()
    try:
        return file_metadata.pop(reference_id)
    finally:
        mutex.release()
