# Import Libraries
import json
from pathlib import Path
from typing import Dict

# Import Schemas
from schemas.state import AnalysisState

# Import Tools
from tools.profiling_tools import (
    detect_sensitive_columns,
    detect_identifier_columns,
    extract_metadata
)
from tools.analysis_tools import (
    get_class_balance,
    get_outlier_summary,
    get_missing_summary,
    get_numerical_summary,
    get_categorical_summary,
    get_correlation_summary,
)

# Import Services
from services.dataset_service import load_dataset, load_col_descriptions
from services.chart_generator import deterministic_charts

# Custom Agents
from agents.insight_agent import write_insights
from agents.reporting_agent import assemble_report
from agents.hypothesis_agent import generate_hypothesis


def load_dataset_node(
    state: AnalysisState
):
    df = load_dataset(state["csv_path"])
    column_descriptions = load_col_descriptions(state["col_descriptions_path"])
    return {
        "df": df,
        "column_descriptions": column_descriptions
    }

def metadata_node(
    state: AnalysisState
):
    df = state["df"]

    sensitive_columns = detect_sensitive_columns(
        df.columns.tolist(),
        state["column_descriptions"]
    ).items

    identifier_columns = detect_identifier_columns(
        df.columns.tolist(),
        state["column_descriptions"]
    ).items

    numerical_columns = list(
        set(
            df.select_dtypes(include = ["number"]).columns
        )
        - set(
            sensitive_columns
            + identifier_columns
            + [state["target"]]
        )
    )

    categorical_columns = list(
        set(
            df.select_dtypes(
                include = ["object", "category"]
            ).columns
        )
        - set(
            sensitive_columns
            + identifier_columns
            + [state["target"]]
        )
    )

    metadata = extract_metadata(
        df,
        numerical_columns,
        categorical_columns,
        state["target"]
    )

    metadata["dataset_name"] = state["dataset_name"]
    metadata["sensitive_columns"] = sensitive_columns
    metadata["identifier_columns"] = identifier_columns
    return {
        "metadata": metadata
    }

def analysis_node(
    state: AnalysisState
):
    df = state["df"]

    numerical_columns = state["metadata"]["features"]["numerical_columns"]
    categorical_columns = state["metadata"]["features"]["categorical_columns"]

    return {
        "missing": get_missing_summary(df),
        "outliers": get_outlier_summary(df, numerical_columns),
        "correlation": get_correlation_summary(df, numerical_columns),
        "class_balance": get_class_balance(df, state["target"]),
        "numerical_distributions": get_numerical_summary(df, numerical_columns),
        "categorical_summary": get_categorical_summary(df, categorical_columns),
    }

def visualization_node(
    state: AnalysisState
):
    return {
        "deterministic_charts": deterministic_charts(state, state["report_folder"])
    }

def insight_node(
    state: AnalysisState
): 
    return {
        "insight_report": write_insights(state)
    }

def hypothesis_node(
    state: AnalysisState
):
    return {
        "hypothesis_result": generate_hypothesis(state)
    }

def reporting_node(
    state: AnalysisState
):
    return {
        "report_path": assemble_report(state)
    }