from __future__ import annotations

import typing as t
from collections.abc import Iterable

from .models import Anime, Character, Staff, User

__all__ = ("PaginatedQuery",)


class PaginatedQuery:
    """
    Represents the paginated results of a query.

    Attributes:
        animes: The [anime](./anime.md)s recieved.
        characters: The [character](./character.md)s recieved.
        staffs: The [staff](./staff.md)s recieved.
        users: The [user](./user.md)s recieved.
    """

    def __init__(self, client, payload):
        self.animes: t.List[Anime] = []
        self.characters: t.List[Character] = []
        self.staffs: t.List[Staff] = []
        self.users: t.List[User] = []

        self._payload = payload
        self._page = -1
        self._client = client
        self._fill_lists()

    def _fill_lists(self):
        list_types = {
            "media": (Anime, "animes"),
            "characters": (Character, "characters"),
            "staff": (Staff, "staffs"),
            "users": (User, "users"),
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
                self._type = list_types[item_type][1]

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

    def walk_animes(self, attribute: str) -> t.Union[list]:
        """
        This method walks through all the animes that were paginated and returns the attribute that was passed in.

        Args:
            attribute (str): The attribute to look for and ultimately return

        Returns:
            A list of the passed attribute from each [anime](./anime.md)
        """
        return [getattr(anime, attribute) for anime in self.animes]

    def walk_characters(self, attribute: str) -> t.Union[list]:
        """
        This method walks through all the characters that were paginated and returns the attribute that was passed in.

        Args:
            attribute (str): The attribute to look for and ultimately return

        Returns:
            A list of the passed attribute from each [character](./character.md)
        """
        return [getattr(character, attribute) for character in self.characters]

    def walk_staffs(self, attribute: str) -> t.Union[list]:
        """
        This method walks through all the staffs that were paginated and returns the attribute that was passed in.

        Args:
            attribute (str): The attribute to look for and ultimately return

        Returns:
            A list of the passed attribute from each [staff](./staff.md)
        """
        return [getattr(staff, attribute) for staff in self.staffs]

    def walk_users(self, attribute: str) -> t.Union[list]:
        """
        This method walks through all the staffs that were paginated and returns the attribute that was passed in.

        Args:
            attribute (str): The attribute to look for and ultimately return

        Returns:
            A list of the passed attribute from each [user](./user.md)
        """
        return [getattr(user, attribute) for user in self.users]

    def from_id(self, id: int) -> t.Optional[t.Union[Anime, Character, Staff]]:
        """
        This method looks through all the characters or animes that were recieved
        and outputs the Anime/Character instance that corresponds to the given id.

        Args:
            id (int): The id to search for.

        Returns:
            The instance that corresponds to the given id.
        """
        search_from = self.animes or self.characters or self.staffs or self.users
        res = self.find(search_from, lambda item: item.id == id) or None
        if res is not None:
            return res[0]

    def __repr__(self) -> str:
        return f"<PaginatedQuery type={self._type}>"

    def __iter__(self) -> t.Generator:
        yield from self.animes or self.characters or self.staffs or self.users

    def __next__(self) -> t.Union[Anime, Character, Staff, User]:
        self._page += 1

        if self._page >= len(self.animes or self.characters):
            raise StopIteration

        try:
            return self.animes[self._page]
        except IndexError:
            return self.characters[self._page]
