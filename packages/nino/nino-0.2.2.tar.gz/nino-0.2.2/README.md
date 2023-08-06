# Basic examples

<u>**Character**</u>
```py
import nino
import asyncio


async def test():
    async with nino.Client() as client:
        paginator = await client.character_search("Nino")
        print(paginator.characters)

asyncio.run(test())
```

<u>**Anime**</u>
```py
import nino
import asyncio


async def test():
    async with nino.Client() as client:
        paginator = await client.anime_search("Overlord", per_page=4)
        for _ in range(4):
            print(await paginator.next())

asyncio.run(test())
```