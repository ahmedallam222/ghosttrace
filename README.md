# 👻 GhostTrace: Unveiling the AI Agent's Unseen Paths

[![PyPI version](https://img.shields.io/pypi/v/ghosttrace.svg)](https://pypi.org/project/ghosttrace/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/ghosttrace.svg)](https://pypi.org/project/ghosttrace/)
[![GitHub Stars](https://img.shields.io/github/stars/ahmedallam222/ghosttrace?style=social)](https://github.com/ahmedallam222/ghosttrace/stargazers)

**GhostTrace** is an innovative Python library designed to bring unparalleled transparency to your AI agents' decision-making processes. It goes beyond merely recording chosen actions, delving into the "roads not taken" – the phantom branches of thought and decision that shape an agent's final output. By capturing these rejected alternatives, tracking their latency, and estimating API costs, GhostTrace provides deep, actionable insights into your agent's internal workings, helping you understand, debug, and optimize its behavior.

<p align="center">
  <img src="./assets/ghosttrace_overview.png" alt="GhostTrace Overview" width="700"/>
  <br>
  <em>Visualizing the accepted path and phantom branches.</em>
</p>

---

## ✨ Features

- **🛤️ Phantom Branch Tracking**: Record every alternative decision your agent considered but rejected, along with the reasons for their rejection. This allows for comprehensive post-hoc analysis of agent reasoning.
- **💰 Cost Estimation**: Automatically calculate estimated USD costs for various Large Language Models (LLMs) such as OpenAI's GPT series and Anthropic's Claude-3 family. This feature helps in optimizing token usage and managing operational expenses.
- **⏱️ Latency Monitoring**: Measure the time taken for each decision branch, both accepted and rejected, providing critical data for performance optimization and identifying bottlenecks.
- **📄 Structured JSON Exports**: Save detailed traces of agent sessions to a structured `.ghost.json` format. These files are easily parsable and can be used for further analysis, visualization, or replaying.
- **💻 Interactive CLI**: GhostTrace includes a powerful command-line interface that allows you to replay agent sessions directly in your terminal. It offers rich, color-coded output, making it easy to visualize the decision flow and inspect phantom branches.

---

## 🚀 Installation

Install GhostTrace via pip:

```bash
pip install ghosttrace
```

---

## 🛠️ Quick Start

### Basic Usage

Integrate GhostTrace into your Python agent code to start tracking decisions and phantom branches:

```python
from ghosttrace.ghost_writer import GhostWriter

# Initialize the writer, specifying an output directory for .ghost.json files
writer = GhostWriter(output_dir=".")

def my_evaluate_fn(decision: str, context: dict) -> dict:
    """A mock evaluation function for agent decisions."""
    if "risky" in decision.lower():
        return {"status": "rejected", "reason": "Decision deemed too risky for current environment."}
    elif "unknown" in decision.lower():
        return {"status": "rejected", "reason": "Insufficient information to proceed."}
    return {"status": "accepted", "result": f"Processed: {decision}"}

# Example 1: Recording an accepted decision
print("\n--- Recording Accepted Decision ---")
accepted_result = writer.evaluate_and_record(
    decision="Refactor small utility function",
    evaluate_fn=my_evaluate_fn,
    context={"module": "utils.py", "priority": "high"},
    input_tokens=500,
    output_tokens=150,
    model="gpt-3.5-turbo"
)
print(f"Accepted Result: {accepted_result}")

# Example 2: Recording a rejected decision with cost and latency tracking
print("\n--- Recording Rejected Decision with Tracking ---")
rejected_result = writer.evaluate_and_record(
    decision="Deploy untested feature to production",
    evaluate_fn=my_evaluate_fn,
    context={"environment": "production", "risk_level": "critical"},
    input_tokens=1200,
    output_tokens=400,
    model="gpt-4-turbo"
)
print(f"Rejected Result: {rejected_result}")

# The trace will be saved to a .ghost.json file in the specified output_dir
print("\nCheck your .ghost.json file for the recorded traces!")
```

### Using the CLI

GhostTrace provides a command-line interface to easily record and replay your agent's traces. This is particularly useful for debugging and understanding agent behavior without diving deep into logs.

```bash
# 1. Run a mock recording session (simulates an agent's decision process)
ghosttrace record --goal "Develop a new user authentication module"

# This will generate a .ghost.json file (e.g., gt_abcdef12.ghost.json)

# 2. Replay the recorded session to see the chosen paths
ghosttrace replay <session_id>.ghost.json

# 3. Replay the session and explicitly show phantom branches (the rejected alternatives)
ghosttrace replay <session_id>.ghost.json --show-phantoms
```

---

## 📊 Supported Models for Cost Tracking

GhostTrace supports cost estimation for a range of popular LLM models. The pricing is based on publicly available information and is updated periodically. You can specify the model used during `evaluate_and_record` to get accurate cost estimates.

| Model Name         | Input Cost (per 1K tokens) | Output Cost (per 1K tokens) |
| :----------------- | :------------------------- | :-------------------------- |
| `gpt-4`            | $0.03                      | $0.06                       |
| `gpt-4-turbo`      | $0.01                      | $0.03                       |
| `gpt-3.5-turbo`    | $0.0005                    | $0.0015                     |
| `claude-3-opus`    | $0.015                     | $0.075                      |
| `claude-3-sonnet`  | $0.003                     | $0.015                      |
| `claude-3-haiku`   | $0.00025                   | $0.00125                    |
| `default`          | $0.002                     | $0.004                      |

---

## 🤝 Contributing

We welcome contributions to GhostTrace! Whether it's reporting bugs, suggesting new features, or submitting code, your help is invaluable. Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) guide for detailed instructions on how to get started.

## 📜 Code of Conduct

To ensure a welcoming and inclusive community, we adhere to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with 👻 by <a href="https://github.com/ahmedallam222">Ahmed Allam</a>
</p>
