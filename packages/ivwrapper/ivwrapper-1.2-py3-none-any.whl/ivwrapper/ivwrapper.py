from aiohttp import ClientSession


class Api:
    def __init__(self):
        self.url = "https://ivall.pl/"

    async def get_joke(self):
        async with ClientSession() as session:
            async with session.get(self.url + "zart") as r:
                response = await r.json()
        return response["url"]

    async def get_meme(self):
        async with ClientSession() as session:
            async with session.get(self.url + "memy") as r:
                response = await r.json()
        return response["url"]
