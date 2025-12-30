"""Deezer API client.

Ce module gère toutes les communications avec l'API Deezer.
On utilise httpx pour les requêtes HTTP asynchrones.

Concept Python à retenir :
- `async/await` : Permet de faire des opérations non-bloquantes.
  Quand on attend une réponse de l'API, Python peut faire autre chose.
- `httpx` : Comme `axios` en JavaScript, mais pour Python.
"""

from typing import Any

import httpx

from deezer_stats.core.config import settings

# URL de base de l'API Deezer
DEEZER_API_BASE = "https://api.deezer.com"


class DeezerClient:
    """Client pour interagir avec l'API Deezer.

    Exemple d'utilisation :
        async with DeezerClient() as client:
            user = await client.get_me()
            print(user["name"])
    """

    def __init__(self, access_token: str | None = None) -> None:
        """Initialise le client avec un token d'accès.

        Args:
            access_token: Token OAuth2 Deezer. Si None, utilise celui de la config.
        """
        self.access_token = access_token or settings.deezer_access_token
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "DeezerClient":
        """Permet d'utiliser `async with DeezerClient() as client:`."""
        self._client = httpx.AsyncClient(base_url=DEEZER_API_BASE)
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Ferme proprement la connexion HTTP."""
        if self._client:
            await self._client.aclose()

    async def _get(self, endpoint: str) -> dict[str, Any]:
        """Effectue une requête GET vers l'API Deezer.

        Args:
            endpoint: Le chemin de l'API (ex: "/user/me")

        Returns:
            La réponse JSON de l'API

        Raises:
            httpx.HTTPError: Si la requête échoue
            ValueError: Si l'API retourne une erreur
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context.")

        response = await self._client.get(
            endpoint,
            params={"access_token": self.access_token},
        )
        response.raise_for_status()

        data = response.json()

        # L'API Deezer retourne les erreurs dans le JSON, pas en HTTP status
        if "error" in data:
            raise ValueError(f"Deezer API error: {data['error']}")

        return data

    # === Endpoints utilisateur ===

    async def get_me(self) -> dict[str, Any]:
        """Récupère le profil de l'utilisateur connecté."""
        return await self._get("/user/me")

    async def get_my_playlists(self, limit: int = 25) -> dict[str, Any]:
        """Récupère les playlists de l'utilisateur."""
        return await self._get(f"/user/me/playlists?limit={limit}")

    async def get_my_tracks(self, limit: int = 25) -> dict[str, Any]:
        """Récupère les titres favoris de l'utilisateur."""
        return await self._get(f"/user/me/tracks?limit={limit}")

    async def get_my_history(self, limit: int = 25) -> dict[str, Any]:
        """Récupère l'historique d'écoute de l'utilisateur."""
        return await self._get(f"/user/me/history?limit={limit}")

    async def get_my_artists(self, limit: int = 25) -> dict[str, Any]:
        """Récupère les artistes favoris de l'utilisateur."""
        return await self._get(f"/user/me/artists?limit={limit}")

    async def get_my_albums(self, limit: int = 25) -> dict[str, Any]:
        """Récupère les albums favoris de l'utilisateur."""
        return await self._get(f"/user/me/albums?limit={limit}")
