"""Command-line interface for deezer-stats."""

import typer
from rich.console import Console

from deezer_stats import __version__

app = typer.Typer(
    name="deezer",
    help="Deezer Stats CLI - Explore your Deezer data",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Show the application version."""
    console.print(f"[bold blue]Deezer Stats[/bold blue] v{__version__}")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind"),
    port: int = typer.Option(8000, help="Port to bind"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
) -> None:
    """Start the FastAPI server."""
    import uvicorn

    console.print(f"[green]Starting server at http://{host}:{port}[/green]")
    uvicorn.run(
        "deezer_stats.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
