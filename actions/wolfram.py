
from hashlib import md5
from urllib.parse import urlsplit, urlencode, unquote_plus, quote
import aiohttp
import disnake

class Wolfram():

    def __init__(self):
        self.appid = "3H4296-5YPAGQUJK7"
        self.salt = "vFdeaRwBTVqdc5CL"
        self.timeout = aiohttp.ClientTimeout(total=10)

    # Calculates WA sig value(md5(salt + concatenated_query)) with pre-known salt
    async def calc_sig(self, query):
        params = list(filter(lambda x: len(x) > 1, list(map(lambda x: x.split("="), query.split("&")))))
        params.sort(key = lambda x: x[0])
        s = self.salt
        for key, val in params:
            s += key + val
        s = s.encode("utf-8")
        return md5(s).hexdigest().upper()

    # Craft valid signed URL
    async def craft_signed_url(self, url):
        (scheme, netloc, path, query, _) = urlsplit(url)
        _query = {"appid": self.appid}
    
        _query.update(dict(list(filter(lambda x: len(x) > 1, list(map(lambda x: list(map(lambda y: unquote_plus(y), x.split("="))), query.split("&")))))))
        query = urlencode(_query)
        _query.update({"sig": await self.calc_sig(query)}) 
        return f"{scheme}://{netloc}{path}?{urlencode(_query)}"

    # Basic request
    async def basic_req(self, query_part, typer="query"):
        async with aiohttp.ClientSession(timeout = self.timeout) as session:
            async with session.get(await self.craft_signed_url(f"https://api.wolframalpha.com/v2/{typer}?{query_part}")) as resp:
                if resp.status == 200:
                    return await resp.json()

    # Simple anwser response
    async def request(self, query):
        result = await self.basic_req(f"input={quote(query, safe='')}&output=json")
        return result
