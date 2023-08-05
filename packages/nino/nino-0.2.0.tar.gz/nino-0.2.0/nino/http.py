from __future__ import annotations

import typing as t

import requests

from .paginator import PaginatedQuery
from .query import Query, QueryOperation, QueryFields

from .ratelimiter import Ratelimiter as limit

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

    def __init__(self, client: Client, session: requests.Session):
        self.session = session
        self.client = client

    @limit(calls=1, time_frame=1.5)
    def post(self, url: str, json: dict, headers: t.Optional[dict] = None):
        if not headers:
            return self.session.post(url, json=json)
        else:
            return self.session.post(url, json=json, headers=headers)

    def query_from(
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
        resp = self.post(self.BASE, json=payload)
        return PaginatedQuery(self, resp.json())

    def _build_query(self, search_type) -> Query:
        user_fields = (
            "id",
            "name",
            "about",
            "bannerImage",
            "avatar {large}",
            "createdAt",
            "updatedAt "
            "siteUrl",
        )

        staff_fields = (
            "id",
            "name {full}",
            "languageV2",
            "image {large}",
            "description",
            "gender",
            "dateOfBirth {year month day}",
            "dateOfDeath {year month day}",
            "age",
        )

        anime_fields = (
            "id",
            "title {romaji english native}",
            "description",
            "averageScore",
            "status",
            "episodes",
            "siteUrl",
            "coverImage {large}",
            "bannerImage",
            "tags {name}",
        )

        character_fields = (
            "id",
            "name {first last}",
            "dateOfBirth {year month day}",
            "age",
            "siteUrl",
            "description",
            "gender",
            "image {large}",
        )

        types = {
            "anime": ("media", anime_fields),
            "character": ("characters", character_fields),
            "staff": ("staff", staff_fields),
            "user": ("users", user_fields),
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
