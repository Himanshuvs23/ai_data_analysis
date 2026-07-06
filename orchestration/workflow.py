# Import Libraries
from langgraph.graph import StateGraph, END

# Import Schemas
from schemas.state import AnalysisState

# Import Nodes
from orchestration.nodes import (
    insight_node,
    metadata_node,
    analysis_node,
    reporting_node,
    hypothesis_node,
    load_dataset_node,
    visualization_node,
)

def build_graph():
    builder = StateGraph(AnalysisState)

    builder.add_node("load", load_dataset_node)
    builder.add_node("metadata", metadata_node)
    builder.add_node("analysis", analysis_node)
    builder.add_node("visualization", visualization_node)
    builder.add_node("insights", insight_node)
    builder.add_node("hypothesis", hypothesis_node)
    builder.add_node("report", reporting_node)

    builder.set_entry_point("load")

    builder.add_edge("load", "metadata")
    builder.add_edge("metadata", "analysis")
    builder.add_edge("analysis", "visualization")
    builder.add_edge("visualization", "insights")
    builder.add_edge("visualization", "hypothesis")
    builder.add_edge("insights", "report")
    builder.add_edge("hypothesis", "report")
    builder.add_edge("report", END)

    return builder.compile()