from aiohttp import ClientSession
from .functions import fetch


class Api:
    def __init__(self):
        self.url = "https://ivall.pl/"

    async def get_joke(self):
        async with ClientSession() as session:
            r = await fetch(session, self.url + "zart")
            r = r.replace("\n", "")
            r = r.replace("\t", "")
        return r

    async def get_meme(self):
        async with ClientSession() as session:
            r = await fetch(session, self.url + "memy")
        return r
