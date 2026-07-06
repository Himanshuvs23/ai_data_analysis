# Import Libraries
import json
import textwrap
from typing import Dict

def executive_summary_prompt(
    metadata: Dict,
    sections: Dict,
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst writing the Executive Summary of a data quality report.
    This summary appears at the top of the report and is the first thing the reader sees.

    DATASET CONTEXT:
    {
        json.dumps(
            {
                "dataset_name": metadata.get("dataset_name", "dataset"),
                "total_rows": metadata["number_of_rows"],
                "total_columns": metadata["number_of_columns"],
                "target_column": metadata.get("target_column"),
                "numerical_columns": metadata.get("numerical_columns", []),
                "categorical_columns": metadata.get("categorical_columns", []),
            }, indent = 2
        )
    }

    SECTION INSIGHTS ALREADY WRITTEN:
    {
        json.dumps(
            {
                "missing_values": sections.get("missing", ""),
                "outliers": sections.get("outliers", ""),
                "correlations": sections.get("correlation", ""),
                "distributions": sections.get("distributions", ""),
                "categorical": sections.get("categorical_summary", ""),
                "class_balance": sections.get("class_balance", ""),
            }, indent = 2
        )
    }

    INSTRUCTIONS:
    - Write 4 to 6 sentences as a cohesive paragraph, not bullet points.
    - This is a synthesis — do not repeat what each section already says in detail.
    - Cover: dataset size, overall data quality, the most important finding from each area,
    and one overarching recommendation.
    - Prioritise the most critical findings — if outliers are the biggest concern, lead with that.
    - If the data is generally clean, say so confidently.
    - Write for a technical audience who will read the full report after this summary.
    - Do not use headers, bullet points, or markdown formatting.
    """).strip()