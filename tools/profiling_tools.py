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

# def detect_sensitive_columns(python -c "import pandas as pd; print(pd.read_csv('data/customers-1000.csv').columns.tolist())"
#     column_names: List[str],
#     column_descriptions: Dict
# ) -> StringL
#         schema = StringList,
#         prompt = sensitive_columns_prompt(column_names, column_descriptions),
#         caller = "Data Profiler"
#     )

# def detect_identifier_columns(
#     column_names: List[str],
#     column_descriptions: Dict
# ) -> StringList:
#     return planner_llm.invoke_structured(
#         schema = StringList,
#         prompt = identifier_columns_prompt(column_names, column_descriptions),
#         caller = "Data Profiler"
#     )

def detect_sensitive_columns(
    column_names: List[str],
    column_descriptions: Dict
) -> StringList:
    """Identify likely PII using column names and descriptions."""
    sensitive_terms = {
        "name", "first_name", "last_name", "full_name",
        "email", "phone", "mobile", "address",
        "date_of_birth", "birth_date", "dob",
        "ssn", "salary", "bank_account", "credit_card",
        "passport", "medical_record", "latitude", "longitude",
        "ip_address"
    }

    matches = []

    for column in column_names:
        normalized = column.lower().strip().replace(" ", "_")
        description = str(
            column_descriptions.get(column, "")
        ).lower()

        name_match = any(
            term in normalized
            for term in sensitive_terms
        )

        description_match = any(
            term.replace("_", " ") in description
            for term in sensitive_terms
        )

        if name_match or description_match:
            matches.append(column)

    print(f"[RULES] Sensitive columns: {matches}", flush=True)
    return StringList(items=matches)


def detect_identifier_columns(
    column_names: List[str],
    column_descriptions: Dict
) -> StringList:
    """Identify likely primary keys and record identifiers."""
    matches = []

    for column in column_names:
        normalized = column.lower().strip().replace(" ", "_")
        description = str(
            column_descriptions.get(column, "")
        ).lower()

        is_identifier = (
            normalized == "id"
            or normalized == "index"
            or normalized.endswith("_id")
            or normalized.endswith("_uuid")
            or "unique identifier" in description
            or "primary key" in description
            or "record identifier" in description
        )

        if is_identifier:
            matches.append(column)

    print(f"[RULES] Identifier columns: {matches}", flush=True)
    return StringList(items=matches)


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