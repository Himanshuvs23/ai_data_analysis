# Import Libraries
from typing import List
from pydantic import BaseModel

class ChartSpec(BaseModel):
    type: str
    col1: str
    col2: str

class ChartSpecs(BaseModel):
    charts: List[ChartSpec]