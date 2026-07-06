# Import Libraries
import pandas as pd
from typing import List, Dict

# Import Services
from services.models import planner_llm

# Import Schemas
from schemas.common import StringList

# Import Prompts
from prompts.analysis_prompt import (
    sensitive_columns_prompt,
    identifier_columns_prompt
)

def detect_sensitive_columns(
    column_names: List[str],
    column_descriptions: Dict
) -> StringList:
    return planner_llm.invoke_structured(
        schema = StringList,
        prompt = sensitive_columns_prompt(column_names, column_descriptions),
        caller = "Data Profiler"
    )

def detect_identifier_columns(
    column_names: List[str],
    column_descriptions: Dict
) -> StringList:
    return planner_llm.invoke_structured(
        schema = StringList,
        prompt = identifier_columns_prompt(column_names, column_descriptions),
        caller = "Data Profiler"
    )

def extract_metadata(
    df: pd.DataFrame,
    numerical_columns: List[str],
    categorical_columns: List[str],
    target: str
) -> Dict:
    tc_df = df[target].copy()
    
    # Missing Values
    missing_val_perts = {}
    for col in df.columns:
        if col not in missing_val_perts:
            missing_val_perts[col] = 0
        missing_val_perts[col] = float(round((df[col].isna().sum() / len(df)) * 100, 2))

    # Metadata
    return {
        'number_of_rows': len(df),
        'number_of_columns': len(df.columns),
        'columns': df.columns.tolist(),
        'features': {
            'numerical_columns': numerical_columns,
            'categorical_columns': categorical_columns,
            'column_dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values_percentages': missing_val_perts
        },
        'number_of_duplicate_rows': int(df.duplicated().sum()),
        'target_column': target,
        'target_column_dtype': str(tc_df.dtype),
        'target_column_summary': {
            'number_of_unique_values': tc_df.nunique(),
            'value_distribution': {
                str(k): round(v, 3)
                for k, v in (
                    tc_df.value_counts(normalize = True).items()
                )
            }
        }
    }