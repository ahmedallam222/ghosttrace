_**Overwriting the file as intended to improve the repository presentation.**_

# 👻 GhostTrace

[![PyPI version](https://img.shields.io/pypi/v/ghosttrace.svg)](https://pypi.org/project/ghosttrace/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/ghosttrace.svg)](https://pypi.org/project/ghosttrace/)

**GhostTrace** is a lightweight Python library designed to record the "roads not taken" by your AI agents. It captures rejected alternatives (phantom branches), tracks their latency, and estimates API costs, providing deep insights into your agent's decision-making process.

---

## ✨ Features

- **🛤️ Phantom Branch Tracking**: Record every alternative decision your agent considered but rejected.
- **💰 Cost Estimation**: Automatically calculate estimated USD costs for various LLM models (GPT-4, Claude-3, etc.).
- **⏱️ Latency Monitoring**: Measure the time taken for each decision branch.
- **📄 JSON Exports**: Save traces to a structured `.ghost.json` format for later analysis or replaying.
- **💻 Interactive CLI**: Replay agent sessions in your terminal with rich, formatted output.

---

## 🚀 Installation

Install GhostTrace via pip:

```bash
pip install ghosttrace
```

---

## 🛠️ Quick Start

### Basic Usage

```python
from ghosttrace.ghost_writer import GhostWriter

# Initialize the writer
writer = GhostWriter(output_dir='.')

def my_evaluate_fn(decision, context):
    # Your logic to evaluate a decision
    if "risky" in decision:
        return {"status": "rejected", "reason": "Too risky for production"}
    return {"status": "accepted"}

# Evaluate and record a decision with tracking
result = writer.evaluate_and_record(
    decision="Update database schema directly",
    evaluate_fn=my_evaluate_fn,
    context={"env": "production"},
    input_tokens=1200,
    output_tokens=400,
    model="gpt-4-turbo"
)
```

### Using the CLI

GhostTrace comes with a built-in CLI to replay your agent's traces:

```bash
# Run a mock recording session
ghosttrace record --goal "Refactor auth module"

# Replay the session
ghosttrace replay <session_id>.ghost.json

# Show phantom branches (the roads not taken)
ghosttrace replay <session_id>.ghost.json --show-phantoms
```

---

## 📊 Supported Models for Cost Tracking

GhostTrace supports cost estimation for popular models including:
- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Custom**: Default pricing available for other models.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to help improve GhostTrace.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with 👻 by <a href="https://github.com/ahmedallam222">Ahmed Allam</a>
</p>
