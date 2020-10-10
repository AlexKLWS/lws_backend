from typing import Optional, List
from pydantic import BaseModel

from lws_backend.pydantic_models.material import Material
from lws_backend.pydantic_models.icon import Icon


class Preview(Material):
    icon: Icon
    url: Optional[str] = None


class PreviewResponse(BaseModel):
    previews: List[Preview]
    pageCount: int
