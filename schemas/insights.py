# Import Libraries
from pydantic import BaseModel

class TextResponse(BaseModel):
    response: str

class HypothesisResult(BaseModel):
    result: bool
    reasoning: str

class InsightReport(BaseModel):
    missing: TextResponse
    outliers: TextResponse
    correlations: TextResponse
    distributions: TextResponse
    categorical: TextResponse
    class_balance: TextResponse