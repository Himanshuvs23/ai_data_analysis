# Import Libraries
import argparse

# Import Custom Modules
from orchestration.run import run_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the AI Data Analyst pipeline."
    )

    parser.add_argument(
        "--dataset-path",
        required = True,
        help = "Path to the input dataset (CSV)."
    )

    parser.add_argument(
        "--column-descriptions",
        required = True,
        help = "Path to the column descriptions JSON."
    )

    parser.add_argument(
        "--target-column",
        required = True,
        help = "Name of the target column."
    )

    parser.add_argument(
        "--dataset-name",
        required = True,
        help = "Display name of the dataset."
    )

    parser.add_argument(
        "--output-folder",
        required = True,
        help = "Directory where the report will be saved."
    )

    args = parser.parse_args()

    report_path = run_pipeline(
        csv_path = args.dataset_path,
        dataset_name = args.dataset_name,
        col_descriptions_path = args.column_descriptions,
        target_column = args.target_column,
        output_folder = args.output_folder,
    )

    print(f"Report saved to: {report_path}")

"""
python main.py
    --dataset-path data/samples/space_titanic/train.csv
    --column-descriptions data/samples/space_titanic/column_descriptions.json
    --target-column transported
    --dataset-name "Space Titanic"
    --output-folder outputs/reports/space_titanic/
"""


# "Remaining"
"""
Narrative/story layer          ← cross-section insight that connects findings
Evaluation loop                ← flag inconclusive insights, suggest new pairs
Column description inference   ← infer_column_descriptions() via LLM
LangGraph orchestrator         ← replace linear pipeline with state machine
Streamlit UI                   ← make it a product
README + demo GIF              ← make it shippable

Must haves:
1. Fix report bugs (14 out of 13 columns, empty boxplots)
2. Streamlit UI
3. README + demo GIF
4. Narrative layer

Nice to haves:
5. Error handling
6. Multi-format input (.xlsx, .parquet)
7. Column description inference
8. LangGraph orchestrator
9. Anthropic API fallback

Polish:
10. Consistent chart styling
11. Report versioning
12. GitHub Actions CI
13. PyPI package
"""