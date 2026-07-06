# Import Libraries
import json
import textwrap
from typing import Dict, List

# Missing Values
def missing_values_prompt(
    missing_summary: Dict,
    metadata: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Missing Values section of a data quality report.

    DATASET CONTEXT:
    {
        json.dumps(
            {
                "dataset_name": metadata.get("dataset_name", "dataset"),
                "total_rows": metadata["number_of_rows"],
                "total_columns": metadata["number_of_columns"],
                "identifier_columns": metadata.get("identifier_columns", []),
                "sensitive_columns": metadata.get("sensitive_columns", []),
            }, indent = 2
        )
    }

    MISSING VALUES DATA:
    {
        json.dumps(missing_summary, indent = 2)
    }

    INSTRUCTIONS:
    - Write 3 to 5 sentences as a cohesive paragraph, not bullet points.
    - Start with the overall picture from summary (how many columns affected, severity).
    - Identify any pattern — is missingness uniform across columns or concentrated?
    - Note if sensitive or identifier columns have missing values.
    - End with a recommendation (e.g. imputation strategy, safe to drop, or no action needed).
    - Do not repeat raw numbers excessively — summarise the pattern instead.
    - Do not use headers or markdown formatting.
    """).strip()

# Outliers
def outliers_prompt(
    outliers: Dict,
    distributions: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Outliers section of a data quality report.

    DISTRIBUTIONS CONTEXT (summary only):
    {
        json.dumps(distributions, indent = 2)
    }

    OUTLIERS DATA:
    {
        json.dumps(outliers, indent = 2)
    }

    INSTRUCTIONS:
    - Write 3 to 5 sentences as a cohesive paragraph, not bullet points.
    - Start with the overall severity picture from summary.
    - Group columns by severity — discuss high severity columns together, low separately.
    - Connect to the distributions context — if median is 0 and outlier % is high,
    explain this suggests a small group of heavy spenders, not data errors.
    - Distinguish between true outliers (data errors) and natural outliers (valid extreme values).
    - End with a recommendation (cap, log-transform, keep, or investigate further).
    - Do not use headers or markdown formatting.
    """).strip()

# Correlations
def correlations_prompt(
    correlation: Dict,
    numerical_columns: List
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Correlations section of a data quality report.

    NUMERICAL COLUMNS:
    {
        json.dumps(numerical_columns, indent = 2)
    }

    CORRELATION DATA:
    {
        json.dumps(correlation, indent = 2)
    }

    INSTRUCTIONS:
    - Write 3 to 5 sentences as a cohesive paragraph, not bullet points.
    - Start with whether any strong correlations exist (multicollinearity concern or not).
    - Discuss notable pairs — what might the relationship mean in the context of the data?
    - If no strong correlations exist, explicitly state this is a positive finding
    (features carry independent information).
    - Do not just list pairs with numbers — interpret what the relationships mean.
    - Do not use headers or markdown formatting.
    """).strip()

# Distributions
def distributions_prompt(
    distributions: Dict,
    outliers_summary: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Distributions section of a data quality report.

    OUTLIERS CONTEXT (summary only):
    {
        json.dumps(outliers_summary, indent = 2)
    }

    DISTRIBUTIONS DATA:
    {
        json.dumps(distributions, indent = 2)
    }

    INSTRUCTIONS:
    - Write 4 to 6 sentences as a cohesive paragraph, not bullet points.
    - Group columns by skewness label — discuss highly skewed columns together,
    symmetric columns separately.
    - For highly skewed columns, interpret what mean >> median means in plain terms
    (e.g. most passengers spend nothing; a small group spends heavily).
    - Connect to outliers context — high skewness and high outlier % tell the same story.
    - Note any columns with min = 0 across the board and what that implies.
    - End with a recommendation (log-transform, standardise, or keep as-is).
    - Do not use headers or markdown formatting.
    """).strip()

# Categorical Summary
def categorical_prompt(
    categorical_summary: Dict,
    metadata: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Categorical Features section of a data quality report.

    DATASET CONTEXT:
    {
        json.dumps(
            {
                "total_rows": metadata["number_of_rows"],
                "identifier_columns": metadata.get("identifier_columns", []),
            }, indent = 2
        )
    }

    CATEGORICAL DATA:
    {
        json.dumps(categorical_summary, indent = 2)
    }

    INSTRUCTIONS:
    - Write 4 to 6 sentences as a cohesive paragraph, not bullet points.
    - Start with the overall picture — how many categorical columns, any high cardinality.
    - For high cardinality columns, note they need special handling (target encoding etc.)
    and should not be one-hot encoded directly.
    - For binary columns, note if they are heavily imbalanced (e.g. vip: 97.7% False).
    - For other columns, interpret the dominant category — what does it tell us about the data?
    - Do not list every category with its percentage — pick the most meaningful observations.
    - Do not use headers or markdown formatting.
    """).strip()

# Class Balance
def class_balance_prompt(
    class_balance: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Class Balance section of a data quality report.

    CLASS BALANCE DATA:
    {json.dumps(class_balance, indent = 2)}

    INSTRUCTIONS:
    - Write 2 to 3 sentences as a cohesive paragraph, not bullet points.
    - State the target column, its class distribution, and the imbalance severity.
    - If balanced: confirm no resampling or class weighting is needed.
    - If imbalanced: recommend specific techniques (SMOTE, class_weight, stratified splits).
    - Keep it concise — this is the simplest section.
    - Do not use headers or markdown formatting.
    """).strip()