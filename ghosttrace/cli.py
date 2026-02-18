"""GhostTrace CLI — Record and replay AI agent decisions."""

import typer
from rich.console import Console

from ghosttrace.mock_agent import run_mock_agent
from ghosttrace.recorder import save_trace
from ghosttrace.replayer import replay

app = typer.Typer(
    name="ghosttrace",
    help="👻 GhostTrace — Record AI agent decisions, including phantom branches.",
    add_completion=False,
)
console = Console()


@app.command()
def record(
    goal: str = typer.Option(
        "Refactor the auth module to use OAuth2",
        "--goal", "-g",
        help="The goal/task for the mock agent.",
    ),
    output: str = typer.Option(
        None,
        "--output", "-o",
        help="Output file path. Defaults to <session_id>.ghost.json",
    ),
) -> None:
    """Run a mock agent and record its decisions to a .ghost.json file."""
    console.print("\n👻 [bold cyan]GhostTrace[/bold cyan] — Recording agent run...\n")

    trace = run_mock_agent(goal=goal)
    path = save_trace(trace, output_path=output)

    steps = trace["summary"]["total_steps"]
    phantoms = trace["summary"]["total_phantoms"]

    console.print(f"  ✅ Recorded [bold]{steps}[/bold] decisions with "
                  f"[bold red]{phantoms}[/bold red] phantom branches.")
    console.print(f"  📄 Saved to [bold green]{path}[/bold green]\n")
    console.print(f"  [dim]Replay with:[/dim]  ghosttrace replay {path}")
    console.print(f"  [dim]See ghosts:[/dim]   ghosttrace replay {path} --show-phantoms\n")


@app.command()
def replay_cmd(
    file: str = typer.Argument(..., help="Path to a .ghost.json file."),
    show_phantoms: bool = typer.Option(
        False,
        "--show-phantoms",
        help="Show phantom branches (rejected alternatives).",
    ),
) -> None:
    """Replay a recorded agent trace from a .ghost.json file."""
    replay(file, show_phantoms=show_phantoms)


# Typer registers commands by function name, so we alias for a clean CLI
app.command(name="replay")(replay_cmd)


if __name__ == "__main__":
    app()
