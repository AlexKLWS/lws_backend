from lws_backend.pydantic_models.material import Material
from lws_backend.pydantic_models.icon import Icon


class ExtMaterial(Material):
    icon: Icon
    url: str
