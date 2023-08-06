from __future__ import annotations

import typing as t
from collections.abc import Iterable

from .models import Anime, Character, Staff, User, Studio

__all__ = ("PaginatedQuery",)


class PaginatedQuery:
    """
    Represents the paginated results of a query.

    Attributes:
        animes: The [anime](./anime.md)s recieved.
        characters: The [character](./character.md)s recieved.
        staffs: The [staff](./staff.md)s recieved.
        studios: The [studio](./studio.md)s recieved.
        users: The [user](./user.md)s recieved.
    """

    def __init__(self, client, payload):
        self.animes: t.List[Anime] = []
        self.characters: t.List[Character] = []
        self.staffs: t.List[Staff] = []
        self.studios: t.List[Studio] = []
        self.users: t.List[User] = []

        self._payload = payload
        self._page = -1
        self._client = client
        self._fill_lists()
        self.pag_type = (
            self.animes or self.characters or self.staffs or self.users or self.studios
        )

    def _fill_lists(self):
        list_types = {
            "media": (Anime, "animes"),
            "characters": (Character, "characters"),
            "staff": (Staff, "staffs"),
            "users": (User, "users"),
            "studios": (Studio, "studios"),
        }
        for item_type in self._payload["data"]["Page"]:
            if item_type in list_types:
                class_type = list_types[item_type][0]
                setattr(
                    self,
                    list_types[item_type][1],
                    [
                        class_type(self._client, data)
                        for data in self._payload["data"]["Page"][item_type]
                    ],
                )
                self._type = list_types[item_type]

    def find(self, iterable: Iterable, check: t.Callable) -> list:
        """
        This method returns a list of results that pass the check function from an iterable

        Args:
            iterable (Iterable): The iterable to search through
            check (t.Callable): The check an item needs to pass

        Returns:
            A list of results that pass the check function

        ```python
        print(paginator.find(paginator.animes, lambda a: a.status == "FINISHED")
        ```
        """
        return [item for item in iterable if check(item)]

    def walk(self, attribute: str, iterable: t.Iterable = None) -> list:
        """
        This method walks through the paginator and returns the attribute that was passed in.
        Args:
            attribute (str): The attribute to look for and ultimately return
            iterable (t.Iterable): The iterable to walk through. Default will auto search for you
        Returns:
            A list of the passed attribute to return from each the instances corresponding to the item in the iterable
        """
        iterable = iterable or self.pag_type
        return [getattr(item, attribute) for item in iterable]

    def from_id(
        self, id: int
    ) -> t.Optional[t.Union[Anime, Character, Staff, User, Studio]]:
        """
        This method looks through all the characters or animes that were recieved
        and outputs the Anime/Character instance that corresponds to the given id.

        Args:
            id (int): The id to search for.

        Returns:
            The instance that corresponds to the given id.
        """
        search_from = (
            self.animes or self.characters or self.staffs or self.users or self.studios
        )
        res = self.find(search_from, lambda item: item.id == id) or None
        if res is not None:
            return res[0]

    async def next(self):
        return await self.__anext__()

    def __repr__(self) -> str:
        return f"<PaginatedQuery type={self._type[1]}>"

    def __aiter__(self) -> PaginatedQuery:
        return self

    async def __anext__(self) -> t.Union[Anime, Character, Staff, User, Studio]:
        self._page += 1

        if self._page >= len(self.pag_type):
            raise StopIteration

        return self.pag_type[self._page]
