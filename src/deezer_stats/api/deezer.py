"""Endpoints pour accéder aux données Deezer.

Concept Python/FastAPI à retenir :
- `APIRouter` : Permet de grouper des endpoints liés ensemble.
  C'est comme créer un "mini-app" qu'on branche sur l'app principale.
- Les fonctions `async def` permettent de gérer plusieurs requêtes en parallèle.
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from deezer_stats.services.deezer import DeezerClient

# Création du router - tous les endpoints ici seront préfixés par "/deezer"
router = APIRouter(prefix="/deezer", tags=["deezer"])


@router.get("/me")
async def get_my_profile() -> dict[str, Any]:
    """Récupère ton profil Deezer."""
    async with DeezerClient() as client:
        try:
            return await client.get_me()
        except ValueError as e:
            # "from e" conserve l'erreur originale dans la stack trace
            raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/playlists")
async def get_my_playlists(limit: int = 25) -> dict[str, Any]:
    """Récupère tes playlists Deezer.

    Args:
        limit: Nombre max de playlists à retourner (défaut: 25)
    """
    async with DeezerClient() as client:
        try:
            return await client.get_my_playlists(limit=limit)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/tracks")
async def get_my_tracks(limit: int = 25) -> dict[str, Any]:
    """Récupère tes titres favoris."""
    async with DeezerClient() as client:
        try:
            return await client.get_my_tracks(limit=limit)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/history")
async def get_my_history(limit: int = 25) -> dict[str, Any]:
    """Récupère ton historique d'écoute."""
    async with DeezerClient() as client:
        try:
            return await client.get_my_history(limit=limit)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/artists")
async def get_my_artists(limit: int = 25) -> dict[str, Any]:
    """Récupère tes artistes favoris."""
    async with DeezerClient() as client:
        try:
            return await client.get_my_artists(limit=limit)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e


@router.get("/albums")
async def get_my_albums(limit: int = 25) -> dict[str, Any]:
    """Récupère tes albums favoris."""
    async with DeezerClient() as client:
        try:
            return await client.get_my_albums(limit=limit)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e
