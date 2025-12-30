"""Command-line interface for deezer-stats.

Ce module utilise Typer (basé sur Click) pour créer des commandes CLI.
Rich est utilisé pour un affichage coloré dans le terminal.

Concept Python à retenir :
- `asyncio.run()` : Permet d'exécuter du code async depuis du code synchrone.
  Les commandes CLI sont synchrones, mais notre client Deezer est async.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from deezer_stats import __version__
from deezer_stats.services.deezer import DeezerClient

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


async def _fetch_all_data() -> dict[str, Any]:
    """Récupère toutes les données Deezer disponibles."""
    async with DeezerClient() as client:
        console.print("[yellow]Récupération de ton profil...[/yellow]")
        profile = await client.get_me()

        console.print("[yellow]Récupération de tes playlists...[/yellow]")
        playlists = await client.get_my_playlists(limit=100)

        console.print("[yellow]Récupération de tes titres favoris...[/yellow]")
        tracks = await client.get_my_tracks(limit=100)

        console.print("[yellow]Récupération de ton historique...[/yellow]")
        history = await client.get_my_history(limit=100)

        console.print("[yellow]Récupération de tes artistes favoris...[/yellow]")
        artists = await client.get_my_artists(limit=100)

        console.print("[yellow]Récupération de tes albums favoris...[/yellow]")
        albums = await client.get_my_albums(limit=100)

        return {
            "exported_at": datetime.now().isoformat(),
            "profile": profile,
            "playlists": playlists,
            "favorite_tracks": tracks,
            "listening_history": history,
            "favorite_artists": artists,
            "favorite_albums": albums,
        }


@app.command()
def dump(
    output: Path = Path("deezer_dump.json"),  # noqa: B008
) -> None:
    """Exporte toutes tes données Deezer dans un fichier JSON.

    Args:
        output: Fichier de sortie (défaut: deezer_dump.json)
    """
    console.print("[bold blue]🎵 Deezer Data Dump[/bold blue]\n")

    try:
        # asyncio.run() exécute la fonction async dans un contexte sync
        data = asyncio.run(_fetch_all_data())
    except ValueError as e:
        console.print(f"[red]Erreur: {e}[/red]")
        console.print("[dim]Vérifie ton token dans .env[/dim]")
        raise typer.Exit(1) from e

    # Sauvegarde dans le fichier JSON
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    console.print(f"\n[green]✓ Données exportées dans {output}[/green]\n")

    # Affiche un résumé
    table = Table(title="Résumé de tes données Deezer")
    table.add_column("Catégorie", style="cyan")
    table.add_column("Nombre", style="magenta", justify="right")

    table.add_row("Playlists", str(data["playlists"].get("total", 0)))
    table.add_row("Titres favoris", str(data["favorite_tracks"].get("total", 0)))
    table.add_row("Artistes favoris", str(data["favorite_artists"].get("total", 0)))
    table.add_row("Albums favoris", str(data["favorite_albums"].get("total", 0)))
    table.add_row("Historique (récent)", str(len(data["listening_history"].get("data", []))))

    console.print(table)


if __name__ == "__main__":
    app()
