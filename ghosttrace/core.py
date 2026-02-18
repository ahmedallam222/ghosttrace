import uuid
from datetime import datetime, timezone
from ghosttrace.tracking import (
    LatencyTimer,
    build_cost_metrics,
)

class GhostTrace:
    def __init__(self, output_dir="."):
        self.output_dir = output_dir
        self._phantom_branches = []

    def _generate_id(self):
        return str(uuid.uuid4())

    def _now_iso(self):
        return datetime.now(timezone.utc).isoformat()

    def record_phantom_branch(
        self,
        decision: str,
        reason: str,
        context: dict = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = "default",
        _latency_ms: float = None,
    ):
        latency = _latency_ms if _latency_ms is not None else 0.0
        metrics = build_cost_metrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency,
            model=model,
        )
        phantom_entry = {
            "id": self._generate_id(),
            "timestamp": self._now_iso(),
            "decision": decision,
            "status": "rejected",
            "reason": reason,
            "context": context or {},
            "tracking": metrics.to_dict(),
        }
        self._phantom_branches.append(phantom_entry)
        self._save_ghost_json()

    def evaluate_and_record(
        self,
        decision: str,
        evaluate_fn: callable,
        context: dict = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = "default",
    ):
        timer = LatencyTimer()
        with timer:
            result = evaluate_fn(decision, context)
        if result.get("status") == "rejected":
            self.record_phantom_branch(
                decision=decision,
                reason=result.get("reason", ""),
                context=context,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=model,
                _latency_ms=timer.elapsed_ms,
            )
        return result

    def _save_ghost_json(self):
        # This will be overridden or implemented in ghost_writer.py
        pass
