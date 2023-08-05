from __future__ import annotations

import typing as t

import requests

from .http import HTTPClient
from .paginator import PaginatedQuery

__all__ = ("Client",)


class Client:
    """
    The client that is used to communicate with the AniList API.

    Attributes:
        token (str, optional): The token used to do mutations on the AniList API.
        session (requests.Session, optional): A session that is used to actually send the requests.
        http (nino.HTTPClient): An HTTPClient instance used to handle every request.
    """

    def __init__(
        self,
        token: t.Optional[str] = None,
        session: t.Optional[requests.Session] = None,
    ):
        self.session = requests.Session() if session is None else session
        self.http = HTTPClient(self, self.session)
        self.token = token

    def anime_search(
        self, name: str, *, page: int = 1, per_page: int = 1
    ) -> PaginatedQuery:
        """
        A method used to query the API for a Anime, with the data provided.

        Args:
            name (str): The name to search for.
            page (int, optional): What page of items to return. Defaults to 1.
            per_page (int, optional): How many items to show per page. Defaults to 1.

        Returns:
            The [PaginatedQuery](./paginator.md) instance used to read the data that was sent back.
        """
        return self.http.query_from(
            name, search_type="anime", page=page, per_page=per_page
        )

    def character_search(
        self, name: str, *, page: int = 1, per_page: int = 1
    ) -> PaginatedQuery:
        """
        A method used to query the API for a Character, with the data provided.

        Args:
            name (str): The name to search for.
            page (int, optional): What page of items to return. Defaults to 1.
            per_page (int, optional): How many items to show per page. Defaults to 1.

        Returns:
            The [PaginatedQuery](./paginator.md) instance used to read the data that was sent back.
        """
        return self.http.query_from(
            name, search_type="character", page=page, per_page=per_page
        )

    def staff_search(
        self, name: str, *, page: int = 1, per_page: int = 1
    ) -> PaginatedQuery:
        """
        A method used to query the API for a Staff, with the data provided.

        Args:
            name (str): The name to search for.
            page (int, optional): What page of items to return. Defaults to 1.
            per_page (int, optional): How many items to show per page. Defaults to 1.

        Returns:
            The [PaginatedQuery](./paginator.md) instance used to read the data that was sent back.
        """
        return self.http.query_from(
            name, search_type="staff", page=page, per_page=per_page
        )

    def user_search(
        self, name: str, *, page: int = 1, per_page: int = 1
    ) -> PaginatedQuery:
        """
        A method used to query the API for a User, with the data provided.

        Args:
            name (str): The name to search for.
            page (int, optional): What page of items to return. Defaults to 1.
            per_page (int, optional): How many items to show per page. Defaults to 1.

        Returns:
            The [PaginatedQuery](./paginator.md) instance used to read the data that was sent back.
        """
        return self.http.query_from(
            name, search_type="user", page=page, per_page=per_page
        )

    def close(self) -> None:
        """
        A method used to close the Session.
        """
        self.session.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, exc_type, exc_value, trace) -> None:
        self.close()
