
import time
from typing import Any, Type
from collections import defaultdict

from langchain_ollama import ChatOllama

from config.settings import (
    LLM_MODEL,
    VLM_MODEL,
    TEMPERATURE,
)


# Set to False if prompts or responses contain sensitive information.
SHOW_PROMPTS = True
SHOW_RESPONSES = True

# Prevent extremely large prompts/responses from flooding the terminal.
MAX_LOG_CHARS = 4000


def _preview(value: Any, max_chars: int = MAX_LOG_CHARS) -> str:
    """Convert LangChain values into readable, truncated terminal output."""
    if hasattr(value, "to_string"):
        try:
            value = value.to_string()
        except Exception:
            pass

    elif hasattr(value, "content"):
        value = value.content

    text = str(value)

    if len(text) > max_chars:
        text = (
            text[:max_chars]
            + f"\n... [truncated; {len(text)} characters total]"
        )

    return text


class AIModel:
    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
    ):
        self.client = ChatOllama(
            model=model,
            temperature=temperature,
            reasoning=False,
            num_predict=100,
            num_ctx=4096,
        )

        self.name = model
        self.total_calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_latency = 0.0

        self.caller_statistics = defaultdict(
            lambda: {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": 0.0,
            }
        )

    def _update_statistics(
        self,
        latency: float,
        caller: str,
        input_tokens: int,
        output_tokens: int,
    ):
        self.total_calls += 1
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_latency += latency

        stats = self.caller_statistics[caller]
        stats["calls"] += 1
        stats["input_tokens"] += input_tokens
        stats["output_tokens"] += output_tokens
        stats["latency"] += latency

    def _log_start(self, caller: str, prompt: Any):
        print("\n" + "=" * 65, flush=True)
        print(f"[LLM START] {caller}", flush=True)
        print(f"[LLM MODEL] {self.name}", flush=True)

        if SHOW_PROMPTS:
            print("\n[LLM PROMPT]", flush=True)
            print(_preview(prompt), flush=True)

        print("\n[LLM WAIT] Waiting for model response...", flush=True)

    def _log_usage(self, response: Any):
        usage = getattr(response, "usage_metadata", {}) or {}

        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        return input_tokens, output_tokens

    def invoke(
        self,
        prompt: Any,
        caller: str = "Unknown",
    ):
        self._log_start(caller, prompt)
        start = time.perf_counter()

        try:
            response = self.client.invoke(prompt)
            latency = time.perf_counter() - start

            input_tokens, output_tokens = self._log_usage(response)

            self._update_statistics(
                latency=latency,
                caller=caller,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            print("\n[LLM OUTPUT]", flush=True)
            if SHOW_RESPONSES:
                print(_preview(response.content), flush=True)

            print(f"\n[LLM DONE] {latency:.2f}s", flush=True)
            print(
                f"[LLM TOKENS] Input: {input_tokens} | "
                f"Output: {output_tokens}",
                flush=True,
            )

            return response

        except Exception as exc:
            latency = time.perf_counter() - start
            print(
                f"\n[LLM ERROR] {caller} failed after "
                f"{latency:.2f}s: {type(exc).__name__}: {exc}",
                flush=True,
            )
            raise

    def invoke_structured(
        self,
        schema: Type,
        prompt: Any,
        caller: str = "Unknown",
    ):
        self._log_start(caller, prompt)
        start = time.perf_counter()

        try:
            structured_model = self.client.with_structured_output(
                schema,
                include_raw=True,
            )

            raw_response = structured_model.invoke(prompt)
            latency = time.perf_counter() - start

            parsed = raw_response.get("parsed")
            raw = raw_response.get("raw")
            parsing_error = raw_response.get("parsing_error")

            input_tokens, output_tokens = self._log_usage(raw)

            self._update_statistics(
                latency=latency,
                caller=caller,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            if parsing_error:
                print(
                    f"\n[LLM PARSE ERROR] {parsing_error}",
                    flush=True,
                )

            print("\n[LLM RAW OUTPUT]", flush=True)
            if SHOW_RESPONSES and raw is not None:
                print(_preview(raw.content), flush=True)

            print("\n[LLM PARSED OUTPUT]", flush=True)
            if SHOW_RESPONSES:
                print(_preview(parsed), flush=True)

            print(f"\n[LLM DONE] {latency:.2f}s", flush=True)
            print(
                f"[LLM TOKENS] Input: {input_tokens} | "
                f"Output: {output_tokens}",
                flush=True,
            )

            if parsing_error:
                raise parsing_error

            if parsed is None:
                raise ValueError(
                    f"{caller}: model returned no parsed structured output."
                )

            return parsed

        except Exception as exc:
            latency = time.perf_counter() - start
            print(
                f"\n[LLM ERROR] {caller} failed after "
                f"{latency:.2f}s: {type(exc).__name__}: {exc}",
                flush=True,
            )
            raise

    @property
    def total_tokens(self):
        return self.input_tokens + self.output_tokens

    @property
    def average_latency(self):
        if self.total_calls == 0:
            return 0.0
        return self.total_latency / self.total_calls

    def statistics(self):
        return {
            "model": self.name,
            "calls": self.total_calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "average_latency": round(self.average_latency, 3),
            "total_latency": round(self.total_latency, 3),
            "by_caller": dict(self.caller_statistics),
        }

    def reset_statistics(self):
        self.total_calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_latency = 0.0
        self.caller_statistics.clear()


planner_llm = AIModel(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
)

planner_vlm = AIModel(
    model=VLM_MODEL,
    temperature=TEMPERATURE,
)
