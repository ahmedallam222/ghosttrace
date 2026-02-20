"""
Cost & latency tracking per phantom branch.
Requested by the Hacker News community.
"""

import time
from dataclasses import dataclass, asdict
from typing import Optional

# Updated pricing as of February 2026
MODEL_PRICING = {
    "gpt-5": {"input": 0.00125, "output": 0.01},
    "gpt-5.2": {"input": 0.00175, "output": 0.01},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-4.6-opus": {"input": 0.005, "output": 0.025},
    "claude-4.6-sonnet": {"input": 0.003, "output": 0.015},
    "claude-4.6-sonnet-thinking": {"input": 0.003, "output": 0.015},
    "o1": {"input": 0.015, "output": 0.06},
    "o3": {"input": 0.01, "output": 0.04},
    "default": {"input": 0.002, "output": 0.004},
}

@dataclass
class PhantomCostMetrics:
    tokens_used: int = 0
    latency_ms: float = 0.0
    estimated_cost_usd: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

class LatencyTimer:
    def __init__(self):
        self._start: Optional[float] = None
        self._end: Optional[float] = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self._end = time.perf_counter()
        return False

    @property
    def elapsed_ms(self) -> float:
        if self._start is None or self._end is None:
            return 0.0
        return round((self._end - self._start) * 1000, 2)

def estimate_cost(input_tokens, output_tokens, model="default"):
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])
    cost = (input_tokens / 1000) * pricing["input"] + \
           (output_tokens / 1000) * pricing["output"]
    return round(cost, 6)

def build_cost_metrics(input_tokens, output_tokens, 
                       latency_ms, model="default"):
    total_tokens = input_tokens + output_tokens
    cost = estimate_cost(input_tokens, output_tokens, model)
    return PhantomCostMetrics(
        tokens_used=total_tokens,
        latency_ms=round(latency_ms, 2),
        estimated_cost_usd=cost,
    )
