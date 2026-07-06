# Import Libraries
from pathlib import Path
from typing import Dict
from datetime import datetime

def format_model_stats(
    stats: Dict[str, Dict],
    dataset_name: str
) -> str:
    lines = []
    lines.append(f"AI Model Usage - {dataset_name}")
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
    stats_path.write_text(formatted_stats, encoding = "utf-8")
    return str(stats_path)