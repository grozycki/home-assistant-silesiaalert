import ssl
from abc import ABC, abstractmethod
from logging import Logger

import aiohttp
import certifi
from aiohttp import TraceRequestStartParams


class HttpClientInterface(ABC):
    @abstractmethod
    async def make_request(self, url: str) -> str:
        pass


class HttpClient(HttpClientInterface):
    def __init__(self, logger: Logger) -> None:
        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(self.__on_request_start)
        trace_config.on_request_end.append(self.__on_request_end)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(
            connector=connector,
            trace_configs=[trace_config],
            timeout=aiohttp.ClientTimeout(total=5)
        )
        self.logger: Logger = logger

    async def make_request(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    async def __on_request_start(
            self,
            session: aiohttp.ClientSession,
            trace_config_ctx,
            params: TraceRequestStartParams
    ) -> None:
        self.logger.debug("Starting request " + params.method + " " + params.url.path)

    async def __on_request_end(self, session: aiohttp.ClientSession, trace_config_ctx, params) -> None:
        self.logger.debug("Ending request " + params.method + " " + params.url.path)
