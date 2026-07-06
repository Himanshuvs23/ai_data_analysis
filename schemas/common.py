# Import Libraries
from typing import List
from pydantic import BaseModel

class StringList(BaseModel):
    items: List[str]