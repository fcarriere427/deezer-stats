"""Script pour explorer les endpoints disponibles de l'API Deezer."""

import asyncio

import httpx

from deezer_stats.core.config import settings

# Endpoints à tester
ENDPOINTS_TO_TEST = [
    "/user/me",
    "/user/me/history",
    "/user/me/tracks",
    "/user/me/charts",
    "/user/me/charts/tracks",
    "/user/me/charts/albums",
    "/user/me/charts/artists",
    "/user/me/recommendations",
    "/user/me/recommendations/tracks",
    "/user/me/flow",
    "/user/me/personal_songs",
    "/user/me/listening_history",
    "/user/me/statistics",
    "/user/me/stats",
]


async def test_endpoint(client: httpx.AsyncClient, endpoint: str) -> dict:
    """Teste un endpoint et retourne le résultat."""
    try:
        response = await client.get(
            f"https://api.deezer.com{endpoint}",
            params={"access_token": settings.deezer_access_token, "limit": 5},
        )
        data = response.json()

        if "error" in data:
            return {"endpoint": endpoint, "status": "ERROR", "detail": data["error"].get("message", "Unknown")}

        # Résumé des données
        if "data" in data:
            return {
                "endpoint": endpoint,
                "status": "OK",
                "total": data.get("total", len(data["data"])),
                "fields": list(data["data"][0].keys()) if data["data"] else [],
            }
        else:
            return {
                "endpoint": endpoint,
                "status": "OK",
                "fields": list(data.keys()),
            }

    except Exception as e:
        return {"endpoint": endpoint, "status": "EXCEPTION", "detail": str(e)}


async def main():
    """Teste tous les endpoints."""
    print("Exploration des endpoints Deezer API\n")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for endpoint in ENDPOINTS_TO_TEST:
            result = await test_endpoint(client, endpoint)

            print(f"\n{result['endpoint']}")
            print(f"  Status: {result['status']}")

            if "total" in result:
                print(f"  Total items: {result['total']}")
            if "fields" in result:
                print(f"  Fields: {', '.join(result['fields'][:10])}")
            if "detail" in result:
                print(f"  Detail: {result['detail']}")

    print("\n" + "=" * 60)
    print("Exploration terminée !")


if __name__ == "__main__":
    asyncio.run(main())
