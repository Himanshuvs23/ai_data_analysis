# Import Libraries
import pandas as pd
from typing_extensions import TypedDict, NotRequired

# Import Custom Schemas
from schemas.insights import InsightReport

class AnalysisState(TypedDict):

    # Input
    csv_path: str
    target: str
    dataset_name: str
    report_folder: str
    col_descriptions_path: str

    # DataFrame
    df: NotRequired[pd.DataFrame]
    column_descriptions: NotRequired[dict]

    # Profiling
    metadata: NotRequired[dict]
    missing: NotRequired[dict]
    outliers: NotRequired[dict]
    correlation: NotRequired[dict]
    class_balance: NotRequired[dict]

    # Analysis
    numerical_distributions: NotRequired[dict]
    categorical_summary: NotRequired[dict]

    # Reporting
    deterministic_charts: NotRequired[dict]
    hypothesis_result: NotRequired[dict]
    insight_report: NotRequired[InsightReport]

    # Output
    report_path: NotRequired[dict]