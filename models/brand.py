from typing import List
from pydantic.dataclasses import dataclass


@dataclass
class Brand:
    id: str

    images = str
    codeProduit: str

    def __init__(self, codeProduit, images):
        self.codeProduit = codeProduit
        self.images += images
    