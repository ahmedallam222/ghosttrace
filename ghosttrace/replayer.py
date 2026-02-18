"""Handles replaying .ghost.json files with rich output."""

import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()


def load_trace(filepath: str) -> dict:
    """Load and return a ghost trace from a .ghost.json file."""
    path = Path(filepath)
    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {filepath}")
        raise SystemExit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def replay(filepath: str, show_phantoms: bool = False) -> None:
    """Replay a ghost trace to the terminal."""
    trace = load_trace(filepath)
    session = trace["session"]
    decisions = trace["decisions"]
    summary = trace["summary"]

    # Header
    console.print()
    console.print(
        Panel(
            f"[bold cyan]GhostTrace Replay[/bold cyan] 👻\n\n"
            f"  Session:  [yellow]{session['id']}[/yellow]\n"
            f"  Agent:    {session['agent']['name']} ({session['agent']['model']})\n"
            f"  Goal:     [italic]{session['goal']}[/italic]\n"
            f"  Steps:    {summary['total_steps']}   |   "
            f"  Phantoms: {summary['total_phantoms']}",
            title="Session Info",
            border_style="cyan",
        )
    )

    # Decisions
    for decision in decisions:
        console.print()
        step = decision["step"]
        ctx = decision["context"]
        chosen = decision["chosen"]

        # Step header
        console.rule(f"[bold]Step {step}[/bold]", style="blue")
        console.print(f"  [dim]{ctx}[/dim]\n")

        # Chosen action
        console.print(
            Panel(
                f"[green bold]✔ {chosen['action']}[/green bold]  →  "
                f"[white]{chosen['target']}[/white]\n"
                f"  [dim]{chosen['reasoning']}[/dim]",
                title="[green]Chosen Action[/green]",
                border_style="green",
            )
        )

        # Phantom branches
        if show_phantoms and decision.get("phantoms"):
            for j, phantom in enumerate(decision["phantoms"], start=1):
                console.print(
                    Panel(
                        f"[red bold]✘ {phantom['action']}[/red bold]  →  "
                        f"[white]{phantom['target']}[/white]\n"
                        f"  [dim italic]Considered:[/dim italic] {phantom['reasoning']}\n"
                        f"  [red]Rejected:[/red]   {phantom['rejection_reason']}",
                        title=f"[red]Phantom {j}[/red] 👻",
                        border_style="red",
                        style="dim",
                    )
                )

    # Footer
    console.print()
    console.rule(style="cyan")
    outcome_color = "green" if summary["outcome"] == "success" else "red"
    console.print(
        f"  Outcome: [{outcome_color} bold]{summary['outcome'].upper()}"
        f"[/{outcome_color} bold]   |   "
        f"{summary['total_steps']} steps, "
        f"{summary['total_phantoms']} phantom branches"
    )
    if not show_phantoms and summary["total_phantoms"] > 0:
        console.print(
            f"\n  [dim]💡 Tip: Re-run with [bold]--show-phantoms[/bold] to see "
            f"{summary['total_phantoms']} rejected alternatives.[/dim]"
        )
    console.print()
