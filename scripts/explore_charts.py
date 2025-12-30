"""Explore le contenu de /user/me/charts/tracks en détail."""

import asyncio
import json

import httpx

from deezer_stats.core.config import settings


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.deezer.com/user/me/charts/tracks",
            params={"access_token": settings.deezer_access_token, "limit": 10},
        )
        data = response.json()

        print("=== TOP 10 TRACKS (charts) ===\n")

        for i, track in enumerate(data.get("data", []), 1):
            print(f"{i}. {track.get('title', 'Unknown')}")
            print(f"   Artiste: {track.get('artist', {}).get('name', 'Unknown')}")
            print(f"   Album: {track.get('album', {}).get('title', 'Unknown')}")
            # Cherchons un compteur d'ecoutes
            print(f"   Rank: {track.get('rank', 'N/A')}")
            print(f"   Tous les champs: {list(track.keys())}")
            print()

        # Sauvegarde le JSON complet pour inspection
        with open("charts_sample.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("JSON complet sauvegarde dans charts_sample.json")


if __name__ == "__main__":
    asyncio.run(main())
