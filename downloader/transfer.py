from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from downloader.state import File
from downloader.schemas import Auth

# ? не лучше ли функциями ?


class Transfer(ABC):
    def __init__(self):
        # ???
        pass

    @abstractmethod
    def check_if_remote_available(self, remote_path: Path, auth: Auth):
        pass

    @abstractmethod
    def download(self, file: File):
        pass

    @abstractmethod
    def upload(self, file: File):
        pass


class HTTPTransfer(Transfer):
    def check_if_remote_available(self, remote_path: Path, auth: Auth):
        pass

    def download(self, file: File):
        pass

    def upload(self, file: File):
        pass


class S3Transfer(Transfer):
    def check_if_remote_available(self, remote_path: Path, auth: Auth):
        pass

    def download(self, file: File):
        pass

    def upload(self, file: File):
        pass
