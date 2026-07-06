# Import Libraries
from typing import Dict

# Import Custom Modules
from orchestration.workflow import build_graph

def run_pipeline(
    csv_path: str,
    dataset_name: str,
    col_descriptions_path: Dict,
    target_column: str,
    output_folder: str,
) -> str:
    
    state = {
        "csv_path": csv_path,
        "dataset_name": dataset_name,
        "col_descriptions_path": col_descriptions_path,
        "target": target_column,
        "report_folder": output_folder,
    }

    graph = build_graph()
    result = graph.invoke(state)
    return result["report_path"]