from pydantic import BaseModel


class Icon(BaseModel):
    data: str
    width: str
    height: str
