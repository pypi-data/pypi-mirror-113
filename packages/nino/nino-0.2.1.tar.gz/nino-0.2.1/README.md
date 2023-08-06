# Basic examples

# Anime search
```py
from nino import Client

with Client() as client:
    paginator = client.anime_search("Overlord")
    print(paginator.animes)
```

# Character search
```py
from nino import Client

with Client() as client:
    paginator = client.character_search("Nino")
    print(paginator.characters)
```