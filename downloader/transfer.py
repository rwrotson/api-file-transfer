from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import aiohttp
import aiofiles
if TYPE_CHECKING:
    from downloader.state import File
from downloader.config import config


class Transfer(ABC):
    def __init__(self, file: 'File'):
        # __enter__ # __exit__
        self.file = file

    @abstractmethod
    def check_if_remote_available(self):
        pass

    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    async def download(self):
        pass

    @abstractmethod
    async def upload(self):
        pass


class HTTPTransfer(Transfer):
    def check_if_remote_available(self):
        pass

    def download(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.file.remote_path) as response:
                length = response.content_length
                async with aiofiles.open(self.file.local_path, mode="wb") as f:
                    async for data in response.content.iter_chunked(config['transfer_settings']['chunk_size']):
                        await f.write(data)

    def upload(self):
        pass


class S3Transfer(Transfer):
    def check_if_remote_available(self):
        pass

    def download(self):
        pass

    def upload(self):
        pass
