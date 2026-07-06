# Import Libraries
import json
import base64
import nbformat
import textwrap
from typing import Dict
from pathlib import Path
from datetime import datetime

# Import Custom Modules
from schemas.state import AnalysisState
from schemas.insights import InsightReport

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
        ""
        f"**Dataset:** {dataset_name}",
        ""
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ""
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
        f"![Distributions]({charts.get('distributions', '')})",
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
        f"![Categorical]({charts.get('categoricals', '')})",
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

    numerical_distribution_charts = []
    for chart in charts["numerical_distribution"].keys():
        chart_path = charts["numerical_distribution"][chart]
        cell = image_cell(report_folder + chart_path)
        numerical_distribution_charts.append(cell)
    
    categorical_distribution_charts = []
    for chart in charts["categorical_distribution"].keys():
        chart_path = charts["categorical_distribution"][chart]
        cell = image_cell(report_folder + chart_path)
        categorical_distribution_charts.append(cell)
    
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
            textwrap.dedent(f"""
            # AI Data Analyst Report \n
            **Dataset:** {dataset_name}\n
            **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}\n
            **Rows:** {metadata["number_of_rows"]} | **Columns:** {metadata["number_of_columns"]}
            """).strip()
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

def format_model_stats(
    stats: Dict[str, Dict],
    dataset_name: str
) -> str:

    lines = []
    lines.append(f"AI Model Usage — {dataset_name}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for model_key, label in [("LLM Model", "LLM"), ("VLM Model", "VLM")]:
        model_stats = stats.get(model_key)
        if not model_stats:
            continue

        lines.append(f"{label} ({model_stats['model']})")
        lines.append(f"  Total calls........... {model_stats['calls']}")
        lines.append(
            f"  Total tokens.......... {model_stats['total_tokens']:,}  "
            f"({model_stats['input_tokens']:,} in / {model_stats['output_tokens']:,} out)"
        )
        lines.append(f"  Total latency......... {model_stats['total_latency']:.2f}s")
        lines.append(f"  Avg latency/call...... {model_stats['average_latency']:.2f}s")
        lines.append("")
        lines.append("  By agent:")

        by_caller = model_stats.get("by_caller", {})
        if by_caller:
            name_width = max(len(name) for name in by_caller) + 2
            for agent_name, agent_stats in by_caller.items():
                agent_tokens = agent_stats["input_tokens"] + agent_stats["output_tokens"]
                lines.append(
                    f"    {agent_name:<{name_width}}"
                    f"{agent_stats['calls']:>2} calls   "
                    f"{agent_tokens:>6,} tokens   "
                    f"{agent_stats['latency']:>7.2f}s"
                )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def save_model_stats(
    stats: Dict[str, Dict],
    output_folder: str,
    dataset_name: str
) -> str:

    formatted_stats = format_model_stats(stats, dataset_name = dataset_name)

    output_dir = Path(output_folder)
    output_dir.mkdir(parents = True, exist_ok = True)
 
    stats_path = output_dir / f"{dataset_name.lower().strip().replace(' ', '_')}_model_stats.txt"
    stats_path.write_text(formatted_stats)
    return str(stats_path)