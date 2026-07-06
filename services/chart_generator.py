# Import Libraries
import pandas as pd
from pathlib import Path
from typing import List, Dict

# Import Schemas
from schemas.state import AnalysisState

# Import Tools
from tools.visualization_tools import (
    plot_bar,
    plot_histogram,
    plot_box_by_target,
    plot_correlation_heatmap,
    plot_2d_scatter_by_class,
    plot_stacked_bar_by_target,
    plot_grouped_bar_by_target
)

def generate_chart(
    df: pd.DataFrame,
    chart_type: str,
    col1: str,
    col2: str,
    target: str,
    output_dir: str,
    numerical: List,
    categorical: List
) -> str:

    chart_path = None
    if chart_type == "scatter":
        chart_path = plot_2d_scatter_by_class(
            x = df[col1],
            y = df[col2],
            target = df[target],
            output_dir = output_dir,
            file_name = f"scatter_{col1}_vs_{col2}",
        )

    elif chart_type == "target_vs_feature":
        if col1 in numerical:
            chart_path = plot_box_by_target(
                feature = df[col1],
                target = df[col2],
                x_label = col2,
                y_label = col1,
                title = f"Boxplot - {col1} by {col2}",
                output_dir = output_dir,
                file_name = f"box_{col1}_vs_target",
                log_scale = False
            )
        elif col1 in categorical:
            chart_path = plot_stacked_bar_by_target(
                feature = df[col1],
                target = df[col2],
                x_label = col1,
                y_label = "Proportion",
                title = f"{col1} by {col2}",
                output_dir = output_dir,
                file_name = f"stacked_{col1}_vs_target",
            )

    elif chart_type == "crosstab":
        chart_path = plot_grouped_bar_by_target(
            feature = df[col1],
            target = df[col2],
            x_label = col1,
            y_label = "Proportion",
            title = f"{col1} vs {col2}",
            output_dir = output_dir,
            file_name = f"crosstab_{col1}_vs_{col2}",
        )
    return chart_path

def deterministic_charts(
    state: AnalysisState,
    output_dir: str,
) -> Dict:

    # Dataframe
    df = state["df"]
    target = state["target"]
    metadata = state["metadata"]

    # Check if directory exists
    Path(output_dir).mkdir(parents = True, exist_ok = True)

    # Create the plot folder
    plots_dir = Path(output_dir) / "plots"
    plots_dir.mkdir(parents = True, exist_ok = True)

    charts = {}

    numerical = metadata["features"]["numerical_columns"]
    categorical = metadata["features"]["categorical_columns"]
    skip_cols = set(metadata.get("identifier_columns", []) + metadata.get("sensitive_columns", []))

    # Missing Values
    if state["missing"]["summary"]["total_missing_columns"] > 0:
        missing_cols = list(state["missing"]["columns"].keys())
        missing_pcts = [state["missing"]["columns"][c]["missing_percentage"] for c in missing_cols]
        charts["missing"] = plot_bar(
            values = missing_pcts,
            labels = missing_cols,
            x_label = "Columns",
            y_label = "Missing %",
            title = "Missing Values by Column",
            output_dir = output_dir,
            file_name = "missing_values"
        )

    # Outliers
    outlier_cols = [
        col for col, v in state["outliers"]["columns"].items()
        if v["severity"] in ("High", "Medium")
    ]
    if outlier_cols:
        outlier_pcts = [state["outliers"]["columns"][c]["outlier_percentage"] for c in outlier_cols]
        charts["outliers"] = plot_bar(
            values = outlier_pcts,
            labels = outlier_cols,
            x_label = "Columns",
            y_label = "Outlier %",
            title = "Outlier Percentage by Column",
            output_dir = output_dir,
            file_name = "outliers"
        )

    # Correlation Heatmap
    charts["correlation"] = plot_correlation_heatmap(
        df = df[numerical],
        columns = numerical,
        title = "Correlation Heatmap",
        output_dir = output_dir,
        file_name = "correlation_heatmap"
    )

    # Class balance
    dist = state["class_balance"]["distribution"]
    charts["class_balance"] = plot_bar(
        values = list(dist.values()),
        labels = list(dist.keys()),
        x_label = "Class",
        y_label = "Proportion",
        title = f"Class Balance - {target}",
        output_dir = output_dir,
        file_name = "class_balance"
    )

    # Boxplot for High/Medium Outlier severity columns
    charts["numerical_distribution"] = {}
    for col in numerical:
        if col in skip_cols:
            continue
        if state["outliers"]["columns"].get(col, {}).get("severity") in ("High", "Medium"):
            skewness_label = state["numerical_distributions"]["columns"].get(col, {}).get("skewness_label", "")
            use_log = skewness_label in ("Highly right-skewed", "Highly left-skewed")

            charts["numerical_distribution"][f"box_{col}"] = plot_box_by_target(
                feature = df[col],
                target = df[target],
                x_label = target,
                y_label = col,
                title = f"Boxplot - {col} by {target}",
                output_dir = output_dir,
                file_name = f"box_{col}_vs_{target}",
                log_scale = use_log
            )
    
    # Histogram per Numerical Column
    for col in numerical:
        if col in skip_cols:
            continue
        charts["numerical_distribution"][f"hist_{col}"] = plot_histogram(
            series = df[col].dropna(),
            col_name = col,
            output_dir = output_dir,
            file_name = f"histogram_{col}",
        )

    # Bar chart per Categorical column
    charts["categorical_distribution"] = {}
    for col in categorical:
        if col in skip_cols:
            continue
        if not state["categorical_summary"]["columns"][col]["is_high_cardinality"]:
            dist = state["categorical_summary"]["columns"][col]["distribution"]
            charts["categorical_distribution"][f"bar_{col}"] = plot_bar(
                values = list(dist.values()),
                labels = list(dist.keys()),
                x_label = col,
                y_label = "Proportion",
                title = f"Distribution - {col}",
                output_dir = output_dir,
                file_name = f"bar_{col}_vs_{target}",
            )
    return charts