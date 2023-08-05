from __future__ import annotations
from socket import socket

import BetterSockets.Asyncio as Asyncio
import BetterSockets.Threads as Threads


class Client:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = Asyncio.Client(**kwargs)

        elif self.__type is False:
            self.__Socket = Threads.Client(**kwargs)

    def send(self, data: str):
        self.__Socket.send(data)
