# Import Libraries
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Import Custom Modules
from schemas.state import AnalysisState

def build_chart_section(
    charts_dict: Dict[str, str],
    report_folder: str
) -> List[str]:
    lines = []
    for chart_name, chart_path in charts_dict.items():
        lines.append(f"**{chart_name}**")
        lines.append("")
        lines.append(f"![{chart_name}]({chart_path})")
        lines.append("")
    return lines

def save_markdown(
    state: AnalysisState,
    executive_summary: str
) -> str:

    metadata = state["metadata"]
    dataset_name = state["dataset_name"]
    insight_report = state["insight_report"]
    charts = state["deterministic_charts"]
    report_folder = state["report_folder"]

    report_lines = [
        "# AI Data Analyst Report",
        "",
        "",
        f"**Dataset:** {dataset_name}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**Rows:** {metadata['number_of_rows']} | **Columns:** {metadata['number_of_columns']}",
        "",
        "---",
        "",
        "## Executive Summary",
        executive_summary.content,
        "",
        "---",
        "",
        "## 1. Missing Values",
        insight_report.missing.response,
        "",
        f"![Missing Values]({charts.get('missing', '')})",
        "",
        "---",
        "",
        "## 2. Outliers",
        insight_report.outliers.response,
        "",
        f"![Outliers]({charts.get('outliers', '')})",
        "",
        "---",
        "",
        "## 3. Distributions",
        insight_report.distributions.response,
        "",
        *build_chart_section(charts.get("numerical_distribution", {}), report_folder),
        "",
        "---",
        "",
        "## 4. Correlations",
        insight_report.correlations.response,
        "",
        f"![Correlations]({charts.get('correlation', '')})",
        "",
        "---",
        "",
        "## 5. Categorical Features",
        insight_report.categorical.response,
        "",
        *build_chart_section(charts.get("categorical_distribution", {}), report_folder),
        "",
        "---",
        "",
        "## 6. Class Balance",
        insight_report.class_balance.response,
        "",
        f"![Class Balance]({charts.get('class_balance', '')})",
        "",
        "---",
        "",
        "## Appendix — Dataset Profile",
        "```json",
        json.dumps(metadata, indent = 2),
        "```",
    ]

    report = "\n".join(report_lines)
    path = Path(report_folder) / f"{dataset_name.lower().strip().replace(' ', '_')}_report.md"
    path.parent.mkdir(parents = True, exist_ok = True)
    path.write_text(report, encoding = "utf-8")
    return str(path)