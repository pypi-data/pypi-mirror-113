from __future__ import annotations

import typing as t

import pathlib
import io
import datetime

if t.TYPE_CHECKING:
    from .client import Client


class Image:
    """
    This class is used to represent an image.
    """

    def __init__(self, client: Client, url: str):
        self._client = client
        self._url = url

    def __repr__(self) -> str:
        return f"<Image url={self._url}>"

    def read(self) -> bytes:
        """
        This method is used to read the image and return the bytes.

        Returns:
            The bytes of the image.
        """
        return self._client.session.get(self._url).content

    def save(self, fp: t.Union[str, pathlib.Path]) -> io.BufferedWriter:
        """
        This method is used to save the image to the specified path.

        Args:
            fp (t.Union[str, pathlib.Path]): The path to save the image to.

        Returns:
            The io.BufferedWriter returned from writing the data.
        """
        data = self.read()
        with open(fp, "wb") as file:
            file.write(data)
            return file

    @property
    def url(self) -> str:
        """
        This attribute represents the actual url of the image recieved from the API.

        Returns:
            The url of the image.
        """
        return self._url


class Anime:
    """
    Represents an Anime object that is recieved from the API.
    """

    def __init__(self, client, payload):
        self._client = client
        self.raw = payload

    def __repr__(self) -> str:
        return f"<Anime name={self.raw['title']['romaji']}>"

    def __str__(self) -> str:
        for name in self.raw["title"].values():
            if name is not None:
                return name
        return "No name"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        The ID assiocated with the Anime.

        Returns:
            The ID recieved from the API.
        """
        return self.raw["id"]

    @property
    def title(self) -> t.Dict[str, str]:
        """
        The titles assiocated with the Anime.

        Returns:
            Contains the native, english and romaji versions of the titles assiocated with the Anime.
        """
        return self.raw["title"]

    @property
    def description(self) -> str:
        """
        The description assiocated with the Anime.

        Returns:
            The description recieved from the API.
        """
        return self.raw["description"]

    @property
    def average_score(self) -> int:
        """
        The average score assiocated with the Anime.

        Returns:
            The score recieved from the API.
        """
        return self.raw["averageScore"]

    @property
    def status(self) -> str:
        """
        The status of the Anime.

        Returns:
            The status recieved from the API.
        """
        return self.raw["status"]

    @property
    def episodes(self) -> int:
        """
        The amount of episodes that the Anime has.

        Returns:
            The amount recieved from the API.
        """
        return self.raw["episodes"]

    @property
    def url(self) -> str:
        """
        The url that corresponds with the Anime.

        Returns:
            The url recieved from the API.
        """
        return self.raw["siteUrl"]

    @property
    def cover_image(self) -> Image:
        """
        Represents the cover image of the Anime.

        Returns:
            The [Image](./image.md) instance that represents the image.
        """
        return Image(self._client, self.raw["coverImage"]["large"])

    @property
    def banner_image(self) -> Image:
        """
        Represents the banner image of the Anime.

        Returns:
            The [Image](./image.md) instance that represents the image.
        """
        return Image(self._client, self.raw["bannerImage"])

    @property
    def tags(self) -> list:
        """
        The list of tags assiocated with the Anime.

        Returns:
            A list of tags recieved from the API.
        """
        return [tag["name"] for tag in self.raw["tags"]]


class Character:
    """
    Represents a Character object recieved from the API.
    """
    def __init__(self, client, payload):
        self._client = client
        self.raw = payload

    def __repr__(self) -> str:
        return (
            f"<Character name={self.raw['name']['first']} {self.raw['name']['last']}>"
        )

    def __str__(self) -> str:
        return f"{self.raw['name']['first']} {self.raw['name']['last']}"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        The ID assiocated with the Character.

        Returns:
            The ID recieved from the API.
        """
        return self.raw["id"]

    @property
    def name(self) -> t.Dict[str, str]:
        """
        The name of the Character.

        Returns:
            The name recieved from the API. Consists of keys such as `first` and `last`.
        """
        return self.raw["name"]

    @property
    def date_of_birth(self) -> t.Dict[str, t.Union[str, int]]:
        """
        The D.O.B of the Character.

        Returns:
            The D.O.B recieved from the API. Consists of keys such as `year`, `month` and `day`.
        """
        return self.raw["dateOfBirth"]

    @property
    def age(self) -> int:
        """
        The age of the Character.

        Returns:
            The age recieved from the API.
        """
        return self.raw["age"]

    @property
    def url(self) -> str:
        """
        The url for the character page on the AniList website

        Returns:
            The url of the character
        """
        return self.raw["siteUrl"]

    @property
    def description(self) -> str:
        """
        The basic description of the Character.

        Returns:
            The description of the character recieved from the API.
        """
        return self.raw["description"]

    @property
    def image(self) -> Image:
        """
        The image of the character

        Returns:
            The [Image](./image.md) instance that represents the image of the character
        """
        return Image(self._client, self.raw["image"]["large"])

    @property
    def gender(self) -> t.Union[str, None]:
        """
        The character's gender. Usually Male, Female, or Non-binary but can be any string.

        Returns:
            The gender recieved from the API.
        """
        return self.raw["gender"]


class Staff:
    """
    Represents a Staff object recieved from the API.
    """
    def __init__(self, client, payload):
        self._client = client
        self.raw = payload

    def __repr__(self) -> str:
        return f"<Staff name={self.name}>"

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        The ID assiocated with the staff.

        Returns:
            The ID recieved from the API.
        """
        return self.raw["id"]

    @property
    def name(self) -> str:
        """
        The name of the staff.

        Returns:
            The full name recieved from the API.
        """
        return self.raw["name"]["full"]

    @property
    def language(self) -> str:
        """
        The language the staff speaks.

        Returns:
            The langauge recieved from the API.
        """
        return self.raw["languageV2"]

    @property
    def image(self) -> Image:
        """
        The image of the staff

        Returns:
            The [Image](./image.md) instance that represents the image of the staff
        """
        return Image(self._client, self.raw["image"]["large"])

    @property
    def description(self) -> str:
        """
        The basic description of the staff.

        Returns:
            The description of the staff recieved from the API.
        """
        return self.raw["description"]

    @property
    def gender(self) -> str:
        """
        The staff's gender. Usually Male, Female, or Non-binary but can be any string.

        Returns:
            The gender recieved from the API.
        """
        return self.raw["gender"]

    @property
    def date_of_birth(self) -> dict:
        """
        The D.O.B of the staff.

        Returns:
            The D.O.B recieved from the API. Consists of keys such as `year`, `month` and `day`.
        """
        return self.raw["dateOfBirth"]

    @property
    def date_of_death(self) -> dict:
        """
        The D.O.D of the staff.

        Returns:
            The D.O.D recieved from the API. Consists of keys such as `year`, `month` and `day`.
        """
        return self.raw["dateOfDeath"]

    @property
    def age(self) -> int:
        """
        The age of the Character.

        Returns:
            The age recieved from the API.
        """
        return self.raw["age"]


class User:
    """
    Represents a User object recieved from the API.
    """
    def __init__(self, client, payload):
        self._client = client
        self.raw = payload

    def __repr__(self) -> str:
        return f"<User name={self.name}>"

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def id(self) -> str:
        """
        The ID assiocated with the user.

        Returns:
            The ID recieved from the API.
        """
        return self.raw["id"]

    @property
    def name(self) -> str:
        """
        The name of the user.

        Returns:
            The name recieved from the API.
        """
        return self.raw["name"]

    @property
    def bio(self) -> str:
        """
        The `about/bio` of the user.

        Returns:
            The about/bio about the user. In markdown form.
        """
        return self.raw["about"]

    @property
    def banner_image(self) -> Image:
        """
        The banner image of the user.

        Returns:
            The [Image](./image.md) instance that represents the corresponding image.
        """
        return Image(self._client, self.raw["bannerImage"])

    @property
    def avatar(self) -> Image:
        """
        The avatar of the user.

        Returns:
            The [Image](./image.md) instance that represents the corresponding image.
        """
        return Image(self._client, self.raw["avatar"]["large"])

    @property
    def url(self) -> str:
        return self.raw["siteUrl"]

    @property
    def created_at(self) -> datetime.datetime:
        """
        The time at which the user's account was created.

        Returns:
            The time recieved from the API.
        """
        return datetime.datetime.fromtimestamp(self.raw["createdAt"])

    @property
    def updated_at(self) -> datetime.datetime:
        """
        The most recent time the user's account was updated at.

        Returns:
            The time recieved from the API.
        """
        return datetime.datetime.fromtimestamp(self.raw["updatedAt"])
