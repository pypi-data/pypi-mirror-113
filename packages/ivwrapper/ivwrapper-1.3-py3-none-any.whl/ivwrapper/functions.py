async def fetch(session, url):
    async with session.get(url) as response:
        r = await response.json()

    return r["url"]
