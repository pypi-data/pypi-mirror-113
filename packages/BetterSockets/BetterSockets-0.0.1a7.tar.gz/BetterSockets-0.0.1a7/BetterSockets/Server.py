from __future__ import annotations
from socket import socket

import BetterSockets.Asyncio as Asyncio
import BetterSockets.Threads as Threads


class ProcessorServer:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = Asyncio.ProcessServer(**kwargs)

        elif self.__type is False:
            self.__Socket = Threads.ProcessServer(**kwargs)

    def listen(self):
        self.__Socket.listen()


class HubServer:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = Asyncio.HubServer(**kwargs)

        elif self.__type is False:
            self.__Socket = Threads.HubServer(**kwargs)

    def listen(self):
        self.__Socket.listen()
