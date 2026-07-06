# Import Libraries
import json
import base64
import nbformat
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Import Custom Modules
from schemas.state import AnalysisState

def image_to_base64(
    image_path: str
) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def md_cell(
    source: str
) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(source)

def code_cell(
    source: str
) -> nbformat.NotebookNode:
    return nbformat.v4.new_code_cell(source)

def image_cell(
    image_path: str
) -> nbformat.NotebookNode:
    try:
        b64 = image_to_base64(image_path)
    except (FileNotFoundError, PermissionError, OSError):
        return md_cell("*Chart not available*")
    return md_cell(f"![chart](data:image/png;base64,{b64})")

def build_image_cells(
    charts: Dict[str, str],
    report_folder: str
) -> List:
    return [
        image_cell(report_folder + chart_path)
        for chart_path in charts.values()
    ]

def save_notebook(
    state: AnalysisState,
    executive_summary: str
) -> str:

    metadata = state["metadata"]
    dataset_name = state["dataset_name"]
    insight_report = state["insight_report"]
    charts = state["deterministic_charts"]
    report_folder = state["report_folder"]
    hypothesis_analysis_result = state["hypothesis_result"]

    nb = nbformat.v4.new_notebook()

    numerical_distribution_charts = build_image_cells(charts["numerical_distribution"], report_folder)
    categorical_distribution_charts = build_image_cells(charts["categorical_distribution"], report_folder)
    
    hypotheses_cells = []
    for hypothesis in hypothesis_analysis_result.keys():
        hypotheses_cells.append(
            md_cell(
                "\n\n".join([
                    f"#### {hypothesis.title()}",
                    f"**Result:** {hypothesis_analysis_result[hypothesis]['result']}",
                    f"**Reasoning:** {hypothesis_analysis_result[hypothesis]['reasoning']}",
                    f"**Evidence:** {hypothesis_analysis_result[hypothesis]['evidence'].content.strip()}",
                ])
            )
        )
        hypotheses_cells.append(
            image_cell(report_folder + hypothesis_analysis_result[hypothesis]["chart"])
        )

    nb.cells = [
        # Title
        md_cell(
            "\n".join([
                "# AI Data Analyst Report",
                "",
                f"**Dataset:** {dataset_name}",
                "",
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "",
                f"**Rows:** {metadata['number_of_rows']} | **Columns:** {metadata['number_of_columns']}",
            ])
        ),

        # Executive summary
        md_cell(f"## Executive Summary\n\n{executive_summary.content}"),

        # Missing values
        md_cell(f"### 1. Missing Values\n\n{insight_report.missing.response}"),
        image_cell(report_folder + charts.get("missing", "")),

        # Outliers
        md_cell(f"### 2. Outliers\n\n{insight_report.outliers.response}"),
        image_cell(report_folder + charts.get("outliers", "")),

        # Distributions
        md_cell(f"### 3. Distributions\n\n{insight_report.distributions.response}"),
        *numerical_distribution_charts,

        # Correlations
        md_cell(f"### 4. Correlations\n\n{insight_report.correlations.response}"),
        image_cell(report_folder + charts.get("correlation", "")),

        # Categorical
        md_cell(f"### 5. Categorical Features\n\n{insight_report.categorical.response}"),
        *categorical_distribution_charts,

        # Class balance
        md_cell(f"### 6. Class Balance\n\n{insight_report.class_balance.response}"),
        image_cell(report_folder + charts.get("class_balance", "")),

        # All Hypothesis
        md_cell(f"### 7. All Tested Hypothesis"),
        *hypotheses_cells,

        # Appendix
        md_cell("## Appendix — Dataset Profile"),
        code_cell(f"import json\nprint(json.dumps({json.dumps(metadata)}, indent = 2))"),
    ]

    path = Path(report_folder) / f"{dataset_name.lower().strip().replace(' ', '_')}_report.ipynb"
    path.parent.mkdir(parents = True, exist_ok = True)
    nbformat.write(nb, str(path))
    return str(path)