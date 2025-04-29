from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class ImageConclusions(BaseModel):
    id: int
    tag: str
    nome: str

class CDI(BaseModel):
    id: int
    url_image: str
    id_Image_conclusions: List[int]

