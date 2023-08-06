import aiohttp

class Session:

    async def get_fact(self,endpoint) -> str:
        async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/facts/{0}".format(endpoint)) as e:
                    js = await e.json()
                    return js['fact']

    async def get_image(self ,endpoint) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/{0}".format(endpoint)) as e:
                js = await e.json()
                return js['link']

    async def get_random_token(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/bottoken") as e:
                js = await e.json()
                return js['token']