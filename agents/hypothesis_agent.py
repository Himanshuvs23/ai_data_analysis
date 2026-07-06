# Import Libraries
from typing import Dict
from langchain_core.messages import HumanMessage

# Import Services
from services.models import (
    planner_llm, planner_vlm
)
from services.chart_generator import generate_chart

# Import Schemas
from schemas.charts import ChartSpec
from schemas.common import StringList
from schemas.state import AnalysisState
from schemas.insights import HypothesisResult

# Import Prompts
from prompts.hypothesis_prompt import (
    hypothesis_chart_prompt,
    hypothesis_insight_prompt,
    hypothesis_generation_prompt,
    hypothesis_evaluation_prompt,
)

# Import tools
from tools.reporting_tools import image_to_base64

# Import global constants
from config.settings import HYPOTHESIS_RETRIES

def get_chart_insight(
    image_path: str,
    report_path: str,
    hypothesis: str,
) -> str:
    b64 = image_to_base64(report_path + image_path)
    message = HumanMessage(
        content = [
            {
                "type": "text",
                "text": hypothesis_insight_prompt(hypothesis),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"},
            },
        ]
    )
    return planner_vlm.invoke(
        prompt = [message],
        caller = "Hypothesis Agent"
    )

def validate_hypothesis(
    hypothesis: str,
    report_folder: str,
    chart_path: str,
) -> Dict:
    # Get visual insight from VLM
    insight = get_chart_insight(
        image_path = chart_path,
        report_path = report_folder,
        hypothesis = hypothesis,
    )

    # Evaluate hypothesis
    evaluation = planner_llm.invoke_structured(
        schema = HypothesisResult,
        prompt = hypothesis_evaluation_prompt(hypothesis, insight),
        caller = "Hypothesis Agent"
    )

    return {
        "result": evaluation.result,
        "reasoning": evaluation.reasoning,
        "evidence": insight,
        "chart": chart_path,
    }

def generate_hypothesis(
    state: AnalysisState
) -> Dict:

    valid_columns = set(state["df"].columns)
    numerical = state["metadata"]["features"]["numerical_columns"]
    categorical = state["metadata"]["features"]["categorical_columns"]
    high_cardinality = set(state["categorical_summary"]["summary"]["high_cardinality_columns"])

    all_hypothesis = {}
    count = 0
    hypothesis_result = {}
    while (count < HYPOTHESIS_RETRIES):

        generated_hypothesis = planner_llm.invoke_structured(
            schema = StringList,
            prompt = hypothesis_generation_prompt(state["metadata"], state["column_descriptions"], all_hypothesis),
            caller = "Hypothesis Agent"
        )

        generated_hypothesis = generated_hypothesis.items
        for hypothesis in generated_hypothesis:
            chart_info = planner_llm.invoke_structured(
                schema = ChartSpec,
                prompt = hypothesis_chart_prompt(hypothesis, state["metadata"]),
                caller = "Hypothesis Agent"
            )

            chart_type = chart_info.type
            col1 = chart_info.col1
            col2 = chart_info.col2
            
            if col1 not in valid_columns or col2 not in valid_columns:
                continue
            if col1 in high_cardinality or col2 in high_cardinality:
                continue

            if (col1 == state["target"]):
                col1, col2 = col2, col1
        
            chart_path = generate_chart(state["df"], chart_type, col1, col2, state["target"], state["report_folder"], numerical, categorical)    
            hypothesis_result[hypothesis] = validate_hypothesis(hypothesis, state["report_folder"], chart_path)
            
            all_hypothesis[hypothesis] = hypothesis_result[hypothesis]['result']
        
        # Increase the count
        count += 1
    
    return hypothesis_result