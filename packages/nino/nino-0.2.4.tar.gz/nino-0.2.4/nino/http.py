from __future__ import annotations

import typing as t
import time
import aiohttp

from .paginator import PaginatedQuery
from .query import Query, QueryOperation, QueryFields
from .fields import ANIME, USER, STUDIO, STAFF, CHARACTER


import asyncio
import logging
import datetime

logger = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("HTTPClient",)


class HTTPClient:
    """
    Used as an interface to communicate to the API

    Attributes:
        session: The session used to send requests
        client: the Client instance being used

    """

    BASE = "https://graphql.anilist.co"

    def __init__(self, client: Client, session: aiohttp.ClientSession):
        self.session = session
        self.client = client
        self._lock = asyncio.Lock()

    async def post(self, url: str, **options: dict):
        json = options.get("json")
        headers = options.get("headers")

        async with self._lock:
            resp = await self.session.post(url, json=json, headers=headers)

        if resp.status == 429:
            await self._lock.acquire()
            reset = (
                datetime.datetime.fromtimestamp(int(resp.headers["X-RateLimit-Reset"]))
                - datetime.datetime.now()
            ).total_seconds()
            print(f"Client is being ratelimited, retrying in {reset}s")
            await asyncio.sleep(float(resp.headers["Retry-After"]))
            self._lock.release()
            return await self.session.post(url, json=json, headers=headers)

        return resp

    async def query_from(
        self, search: str, *, search_type: str, per_page: int = 1, page: int = 1
    ) -> PaginatedQuery:
        """
        A method used to send a query and then recieve back data

        Args:
            search_type (str): What types to search for.
            search (str): query the API and find the data corresponding with the search.
            per_page (int, optional): How many items to recieve per page. Defaults to 1.
            page (int, optional): What page of items to recieve. Defaults to 1.

        Returns:
            PaginatedQuery: The PaginatedQuery instance used to sort and handle the data recieved.
        """
        payload = {
            "query": self._build_query(search_type).build(),
            "variables": {"search": search, "perPage": per_page, "page": page},
        }
        resp = await self.post(self.BASE, json=payload)
        return PaginatedQuery(self, await resp.json())

    def _build_query(self, search_type) -> Query:
        types = {
            "anime": ("media", ANIME),
            "character": ("characters", CHARACTER),
            "staff": ("staff", STAFF),
            "user": ("users", USER),
            "studio": ("studios", STUDIO),
        }
        operation = QueryOperation(
            "query", variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
        )
        fields = QueryFields("Page", page="$page", perPage="$perPage")
        fields.add_field(
            "pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage"
        )
        fields.add_field(
            f"{types[search_type][0]} (search: $search)",
            *types[search_type][1],
        )
        return Query(operation=operation, fields=fields)
