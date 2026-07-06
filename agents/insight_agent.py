# Import Services
from services.models import planner_llm

# Import Schemas
from schemas.insights import (
    TextResponse,
    InsightReport
)
from schemas.state import AnalysisState

# Import Prompts
from prompts.insight_prompt import (
    outliers_prompt,
    categorical_prompt,
    correlations_prompt,
    class_balance_prompt,
    distributions_prompt,
    missing_values_prompt
)

def write_insights(
    state: AnalysisState
) -> InsightReport:
    return InsightReport(
        missing = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = missing_values_prompt(
                missing_summary = state["missing"],
                metadata = state["metadata"]
            ),
            caller = "Insight Agent"
        ),
        outliers = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = outliers_prompt(
                outliers = state["outliers"],
                distributions = state["numerical_distributions"]["summary"]
            ),
            caller = "Insight Agent"
        ),
        correlations = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = correlations_prompt(
                correlation = state["correlation"],
                numerical_columns = state["metadata"]["features"]["numerical_columns"],
            ),
            caller = "Insight Agent"
        ),
        distributions = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = distributions_prompt(
                distributions = state["numerical_distributions"],
                outliers_summary = state["outliers"]["summary"],
            ),
            caller = "Insight Agent"
        ),
        categorical = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = categorical_prompt(
                categorical_summary = state["categorical_summary"],
                metadata = state["metadata"],
            ),
            caller = "Insight Agent"
        ),
        class_balance = planner_llm.invoke_structured(
            schema = TextResponse,
            prompt = class_balance_prompt(
                class_balance = state["class_balance"],
            ),
            caller = "Insight Agent"
        ),
    )