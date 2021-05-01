import asyncio
import typing

from vkwave.client import AIOHTTPClient
from vkwave.api import API as LibAPI
from vkwave.api.token import Token
from vkwave.api.token.token import UserSyncSingleToken
from vkwave.api import APIOptionsRequestContext


class API:
    def __init__(self, token: str, api_version: typing.Optional[str] = None):
        client = AIOHTTPClient()
        token = UserSyncSingleToken(Token(token))
        self._api = LibAPI(tokens=token, clients=client, api_version=api_version)

    def get_api(self) -> APIOptionsRequestContext:
        return self._api.get_context()

    async def close(self) -> None:
        await self._api.default_api_options.clients[0].close()


class SyncAPI:
    def __init__(self, token: str):
        self._api = API(token)

    def api_request(self, _method: str, **kwargs):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError("'SyncAPI' can't be used with already running asyncio event loop")
        return loop.run_until_complete(self._api.get_api().api_request(_method, kwargs))


def run(f):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f)
