__all__ = (
    "STUDIO",
    "ANIME",
    "USER",
    "STAFF",
    "CHARACTER",
)

USER = (
    "id",
    "name",
    "about",
    "bannerImage",
    "avatar {large}",
    "createdAt",
    "updatedAt " "siteUrl",
)

STAFF = (
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

CHARACTER = (
    "id",
    "name {first last}",
    "dateOfBirth {year month day}",
    "age",
    "siteUrl",
    "description",
    "gender",
    "image {large}",
)

ANIME = (
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
    "trailer {site id}",
    "characters (sort: ROLE) {edges {node{.}}}".replace(".", " ".join(CHARACTER)),
    "staff (sort: ROLE) {edges {node{.}}}".replace(".", " ".join(STAFF)),
)

ANIME_S = (
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
    "trailer {site id}",
    "characters (sort: ROLE) { nodes {.} }".replace(".", " ".join(CHARACTER)),
    "staff (sort: ROLE) { nodes {.} }".replace(".", " ".join(STAFF)),
)

STUDIO = (
    "id",
    "name",
    "siteUrl",
    "media (sort: POPULARITY) {edges{ node {..}} }".replace("..", " ".join(ANIME_S)),
)
