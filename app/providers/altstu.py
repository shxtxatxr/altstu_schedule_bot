import httpx


ALTSTU_GROUP_SEARCH_URL = "https://www.altstu.ru/m/s/ajax/"
ALTSTU_SCHEDULE_URL = "https://www.altstu.ru/main/schedule/"


async def search_groups(query: str) -> list[dict]:
    query = query.strip()

    if not query:
        return []

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
        headers={
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0",
        },
    ) as client:
        response = await client.get(
            ALTSTU_GROUP_SEARCH_URL,
            params={"query": query},
        )

        response.raise_for_status()

    return response.json()


async def get_schedule_page(group_id: str) -> str:
    url = f"{ALTSTU_SCHEDULE_URL}{group_id}/"

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    ) as client:
        response = await client.get(url)

        response.raise_for_status()

    return response.text