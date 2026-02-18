# GhostTrace 👻 — AI Agent Decision Recorder

GhostTrace is a Python CLI tool designed to record AI agent decisions, including "Phantom Branches" — the actions the agent considered but ultimately rejected.

## Features
- **Decision Tracking**: Record every step an agent takes.
- **Phantom Branches**: Capture the "roads not taken" and the reasons for rejection.
- **Rich Replay**: Visualize the decision process in a clean, color-coded terminal UI.

## Installation

```bash
pip install -e .
```

## Usage

### Record a session
```bash
ghosttrace record
```

### Replay a session
```bash
ghosttrace replay <session_id>.ghost.json
```

### Replay with Phantom Branches
```bash
ghosttrace replay <session_id>.ghost.json --show-phantoms
```
