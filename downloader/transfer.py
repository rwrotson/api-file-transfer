import os
from abc import ABC, abstractmethod
from pathlib import Path
import aiohttp
import aiofiles

from downloader.enums import Status
from downloader.auth import Auth
from downloader.config import config
from downloader.exceptions import RemotePathNotAvailable


class FileTransfer(ABC):
    def __init__(self, local_path: Path, remote_path: str, auth: Auth):
        self._local_path = local_path
        self._remote_path = remote_path
        self._auth = auth

        self.status: Status = Status.QUEUED
        self._size: int = await self.get_size()  # sync request?
        self._completed: int = 0
        self._resumable: bool = await self.is_resumable()

    @abstractmethod
    async def check_if_remote_available(self) -> None:
        pass

    @abstractmethod
    async def is_resumable(self) -> bool:
        pass

    @abstractmethod
    async def get_size(self) -> int:
        pass

    @abstractmethod
    async def download(self) -> None:
        pass

    @abstractmethod
    async def upload(self) -> None:
        pass

    @property
    def local_path(self):
        return self._local_path

    @property
    def remote_path(self):
        return self._remote_path

     def __eq__(self, other):
         return (self.local_path == other.local_path and
                 self.remote_path == other.remote_path)


class HTTPTransfer(FileTransfer):
    # aenter, aexit?
    async def check_if_remote_available(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.head(self._remote_path) as response:
                if not response.ok:
                    raise RemotePathNotAvailable('Remote path is not available')

    async def is_resumable(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.head(self._remote_path) as response:
                return {'Accept-Ranges': 'bytes'} in response.headers

    async def get_size(self) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._remote_path) as response:
                return response.content_length

    async def download(self) -> None:
        chunk_size = config['transfer_settings']['chunk_size']

        if self._local_path.exists():
            completed = os.stat(self._local_path).st_size
            mode = 'ab'
        else:
            completed = 0
            mode = 'wb'

        range_header = {'Range': f'bytes={completed}-'}

        async with aiohttp.ClientSession(headers=range_header) as session:
            async with session.get(self._remote_path) as response:
                if not self._resumable:
                    self._completed = 0
                    mode = 'wb'
                async with aiofiles.open(self._local_path, mode=mode) as f:
                    async for data in response.content.iter_chunked(chunk_size):
                        await f.write(data)
                        self._completed += len(data)

    def upload(self) -> None:
        pass


class S3Transfer(FileTransfer):
    def check_if_remote_available(self) -> None:
        pass

    def is_resumable(self) -> bool:
        pass

    def get_size(self) -> int:
        pass

    def download(self) -> None:
        pass

    def upload(self) -> None:
        pass
