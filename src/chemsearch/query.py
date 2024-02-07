import asyncio
from typing import Any

import aiohttp


async def get_response_json(session: aiohttp.ClientSession, url: str) -> Any:
    """Get JSON from HTTP get request.

    Args:
        session (aiohttp.ClientSession): Session.
        url (str): URL.

    Returns:
        Any: Response.
    """
    async with session.get(url) as resp:
        data = await resp.json()
        return data


async def query_cluster(urls: list[str]) -> list[str]:
    """Query all URLs asynchronously and aggregate hits.

    Args:
        urls (list[str]): URLs to query.

    Returns:
        list[str]: Hits.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get_response_json(session, url)) for url in urls]

        hits = await asyncio.gather(*tasks)

        return hits
