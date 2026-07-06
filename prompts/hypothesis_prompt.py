# Import Libraries
import json
import textwrap
from typing import Dict

def hypothesis_generation_prompt(
    metadata: Dict,
    column_descriptions: Dict,
    tested_hypotheses: Dict
) -> str:
    hypotheses = ""
    if tested_hypotheses:
        hypotheses = f"""
        TESTED HYPOTHESIS:
        {json.dumps(tested_hypotheses, indent = 2)}
        """

    return textwrap.dedent(f"""
    You are a data analyst generating hypotheses for a dataset.

    DATASET CONTEXT:
    {
        json.dumps(
            {
                "target_column": metadata.get("target_column"),
                "numerical_columns": metadata.get("features", {}).get("numerical_columns", []),
                "categorical_columns": metadata.get("features", {}).get("categorical_columns", []),
            },
            indent = 2
        )
    }

    COLUMN DESCRIPTIONS:
    {json.dumps(column_descriptions, indent = 2)}

    {hypotheses}

    INSTRUCTIONS:
    - Generate 3 to 5 testable hypotheses about relationships in this dataset.
    - Each hypothesis should involve the target column where possible.
    - Frame each as "We hypothesize that [X] because [reasoning]."
    - Base hypotheses on column descriptions and domain context, not statistics.
    - Do not use headers or markdown formatting.
    - Return ONLY a JSON array of hypothesis strings.
    """).strip()

def hypothesis_chart_prompt(
  hypothesis: str,
  metadata: Dict
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst deciding how to best visualize a hypothesis.

    HYPOTHESIS:
    {hypothesis}

    AVAILABLE COLUMNS:
    {
      json.dumps(
        {
          "numerical_columns": metadata["features"]["numerical_columns"],
          "categorical_columns": metadata["features"]["categorical_columns"],
          "target_column": metadata["target_column"],
          "identifier_columns": metadata.get("identifier_columns", []),
          "sensitive_columns": metadata.get("sensitive_columns", []),
        },
        indent = 2
      )
    }

    AVAILABLE CHART TYPES:
    - scatter : {{"type": "scatter", "col1": "<numerical_col>", "col2": "<numerical_col>"}}
    - target_vs_feature : {{"type": "target_vs_feature", "col1": "<feature_col>", "col2": "<target_col>"}}
    - crosstab : {{"type": "crosstab", "col1": "<categorical_col>", "col2": "<categorical_col>"}}

    INSTRUCTIONS:
    - Return ONLY a single JSON object. No explanation whatsoever after the JSON.
    - Only use column names that exist EXACTLY in AVAILABLE COLUMNS. Do not invent columns.
    - Choose the chart type based on column types:
      * Both columns numerical → scatter
      * One categorical, one is target → crosstab
      * One numerical/categorical, other is target → target_vs_feature
    - No explanation, no markdown, no preamble, no text after the JSON object.
    """).strip()

def hypothesis_insight_prompt(
    hypothesis: str
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst evaluating a hypothesis by looking at a chart.
    HYPOTHESIS:
    {hypothesis}

    INSTRUCTIONS:
    - Write 2 to 3 sentences describing what the chart shows.
    - State whether the visual evidence supports or contradicts the hypothesis.
    - Be specific about what you observe in the chart.
    - Do not use headers or markdown formatting.
    """).strip()

def hypothesis_evaluation_prompt(
    hypothesis: str,
    insight: str
) -> str:
    return textwrap.dedent(f"""
    You are a data analyst evaluating whether a hypothesis is supported by visual evidence.

    HYPOTHESIS:
    {hypothesis}

    VISUAL EVIDENCE:
    {insight}

    INSTRUCTIONS:
    - Return ONLY a valid JSON object with exactly two keys:
    {{"result": true/false, "reasoning": "<one sentence>"}}
    - result: true if the evidence supports the hypothesis, false if it contradicts it.
    - reasoning: one sentence explaining why based on the visual evidence.
    - No explanation, no markdown, no preamble, no text after the JSON object.
    """).strip()