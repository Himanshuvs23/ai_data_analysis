
import time
from typing import Dict

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

    print("\n" + "=" * 60, flush=True)
    print(f"AI DATA ANALYST: {dataset_name}", flush=True)
    print("=" * 60, flush=True)

    graph = build_graph()
    started = time.perf_counter()
    node_started = {}
    result = None

    print("[INFO] Graph built. Starting execution...", flush=True)

    try:
        for mode, event in graph.stream(
            state,
            stream_mode=["debug", "values"],
        ):
            if mode == "debug" and isinstance(event, dict):
                event_type = event.get("type")
                payload = event.get("payload", {})
                node = payload.get("name", "unknown")

                if event_type == "task":
                    node_started[node] = time.perf_counter()
                    print(
                        f"\n[START] {node}",
                        flush=True,
                    )

                elif event_type == "task_result":
                    elapsed = (
                        time.perf_counter()
                        - node_started.pop(node, time.perf_counter())
                    )

                    if payload.get("error"):
                        print(
                            f"[FAILED] {node}: {payload['error']}",
                            flush=True,
                        )
                    else:
                        print(
                            f"[DONE] {node} in {elapsed:.2f}s",
                            flush=True,
                        )

            elif mode == "values":
                result = event

    except KeyboardInterrupt:
        print("\n[STOPPED] Pipeline interrupted by user.", flush=True)
        raise

    except Exception as exc:
        print(
            f"\n[ERROR] {type(exc).__name__}: {exc}",
            flush=True,
        )
        raise

    total = time.perf_counter() - started

    if not isinstance(result, dict) or "report_path" not in result:
        keys = list(result.keys()) if isinstance(result, dict) else []
        raise RuntimeError(
            f"No report_path in final state. Available keys: {keys}"
        )

    print("\n" + "=" * 60, flush=True)
    print(f"[SUCCESS] Completed in {total:.2f}s", flush=True)
    print(f"[REPORT] {result['report_path']}", flush=True)
    print("=" * 60, flush=True)

    return result["report_path"]
