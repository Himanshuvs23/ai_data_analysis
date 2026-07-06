# Import Libraries
import time
from typing import Any, Type
from collections import defaultdict
from langchain_ollama import ChatOllama

# Import global constants
from config.settings import (
    LLM_MODEL,
    VLM_MODEL,
    TEMPERATURE,
)

class AIModel:
    def __init__(
        self,
        model: str,
        temperature: float = 0.0
    ):
        self.client = ChatOllama(
            model = model,
            temperature = temperature
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
        output_tokens: int
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

    def invoke(
        self,
        prompt: Any,
        caller: str = "Unknown",
    ):
        start = time.perf_counter()
        response = self.client.invoke(prompt)
        latency = time.perf_counter() - start

        usage = getattr(response, "usage_metadata", {}) or {}
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        self._update_statistics(
            latency = latency,
            caller = caller,
            input_tokens = input_tokens,
            output_tokens = output_tokens
        )
        return response

    def invoke_structured(
        self,
        schema: Type,
        prompt: Any,
        caller: str = "Unknown",
    ):
        start = time.perf_counter()

        structured_model = self.client.with_structured_output(
            schema,
            include_raw = True,
        )
        raw_response = structured_model.invoke(prompt)
        latency = time.perf_counter() - start

        parsed = raw_response["parsed"]
        raw = raw_response["raw"]

        usage = getattr(raw, "usage_metadata", {}) or {}
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        self._update_statistics(
            latency = latency,
            caller = caller,
            input_tokens = input_tokens,
            output_tokens = output_tokens
        )
        return parsed

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
    model = LLM_MODEL,
    temperature = TEMPERATURE
)

planner_vlm = AIModel(
    model = VLM_MODEL,
    temperature = TEMPERATURE
)