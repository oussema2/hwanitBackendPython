from typing import List
from pydantic import BaseModel


class Images(BaseModel):
    id: str

    images = []
    codeProduit: str
