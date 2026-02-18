"""
A dummy agent that simulates decision-making with phantom branches.
Swap this out for a real agent later.
"""

import random
import uuid
from datetime import datetime, timezone


MOCK_DECISIONS = [
    {
        "context": "Agent is deciding how to approach the auth refactor.",
        "chosen": {
            "action": "read_file",
            "target": "src/auth.py",
            "reasoning": "Need to understand current auth implementation first.",
        },
        "phantoms": [
            {
                "action": "search_codebase",
                "target": "grep 'auth' --recursive",
                "reasoning": "Scan the whole codebase for auth references.",
                "rejection_reason": "Too broad; better to start with the known entry point.",
            },
            {
                "action": "write_file",
                "target": "src/auth_oauth2.py",
                "reasoning": "Start writing the new OAuth2 module immediately.",
                "rejection_reason": "Premature — haven't read existing code yet.",
            },
        ],
    },
    {
        "context": "Agent has read auth.py. Deciding next step.",
        "chosen": {
            "action": "write_file",
            "target": "src/auth_oauth2.py",
            "reasoning": "Create new OAuth2 module based on understood structure.",
        },
        "phantoms": [
            {
                "action": "edit_file",
                "target": "src/auth.py",
                "reasoning": "Modify existing file in-place.",
                "rejection_reason": "Risky — better to create new file and migrate.",
            },
        ],
    },
    {
        "context": "New OAuth2 module written. Deciding how to handle migration.",
        "chosen": {
            "action": "edit_file",
            "target": "src/routes.py",
            "reasoning": "Update route imports to point to new auth module.",
        },
        "phantoms": [
            {
                "action": "delete_file",
                "target": "src/auth.py",
                "reasoning": "Remove old auth module immediately.",
                "rejection_reason": "Too aggressive — need to update consumers first.",
            },
            {
                "action": "run_command",
                "target": "python -m pytest",
                "reasoning": "Run tests before changing imports.",
                "rejection_reason": "Tests will fail anyway since new module isn't wired up yet.",
            },
        ],
    },
    {
        "context": "Routes updated. Final verification step.",
        "chosen": {
            "action": "run_command",
            "target": "python -m pytest tests/",
            "reasoning": "Verify everything works end-to-end after migration.",
        },
        "phantoms": [
            {
                "action": "run_command",
                "target": "python -m pytest tests/test_auth.py",
                "reasoning": "Run only auth tests for speed.",
                "rejection_reason": "Migration could break non-auth routes too; full suite is safer.",
            },
        ],
    },
]


def run_mock_agent(goal: str = "Refactor the auth module to use OAuth2") -> dict:
    """Simulate an agent run and return a ghost trace dict."""
    session_id = f"gt_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    decisions = []
    for i, mock in enumerate(MOCK_DECISIONS, start=1):
        decisions.append(
            {
                "step": i,
                "timestamp": (now).isoformat(),
                "context": mock["context"],
                "chosen": mock["chosen"],
                "phantoms": mock["phantoms"],
            }
        )

    total_phantoms = sum(len(d["phantoms"]) for d in decisions)

    return {
        "version": "0.1",
        "session": {
            "id": session_id,
            "timestamp": now.isoformat(),
            "agent": {
                "name": "mock-agent",
                "model": "gpt-4o-mock",
                "version": "0.1.0",
            },
            "goal": goal,
        },
        "decisions": decisions,
        "summary": {
            "total_steps": len(decisions),
            "total_phantoms": total_phantoms,
            "outcome": "success",
        },
    }
