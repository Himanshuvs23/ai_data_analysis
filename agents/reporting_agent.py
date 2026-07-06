# Import Libraries
from typing import Dict

# Import Custom Modules
from services.models import planner_llm, planner_vlm
from schemas.state import AnalysisState
from schemas.insights import InsightReport
from prompts.reporting_prompt import executive_summary_prompt
from tools.reporting_tools import (
    save_markdown, 
    save_notebook,
    save_model_stats
)

# Executive Summary
def write_executive_summary(
    metadata: Dict,
    sections: InsightReport
) -> str:
    prompt = executive_summary_prompt(
        metadata = metadata,
        sections = sections.model_dump(),
    )
    return planner_llm.invoke(
        prompt = prompt,
        caller = "Reporting Agent"
    )

# Main Entry 
def assemble_report(
    state: AnalysisState
) -> Dict:
    executive_summary = write_executive_summary(state["metadata"], state["insight_report"])

    md_path = save_markdown(state, executive_summary)
    nb_path = save_notebook(state, executive_summary)
    model_stats_path = save_model_stats(
        {
            "LLM Model": planner_llm.statistics(),
            "VLM Model": planner_vlm.statistics()
        },
        state["report_folder"],
        state["dataset_name"]
    )

    return {
        "markdown": md_path,
        "notebook": nb_path,
        "model_stats": model_stats_path
    }