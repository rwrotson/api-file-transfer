from uuid import uuid4, UUID
from abc import ABC, abstractmethod

from downloader.transfer import FileTransfer, HTTPTransfer, S3Transfer
from downloader.auth import Auth
from downloader.enums import Status, TransferProtocol
from downloader.exceptions import (
    PathNotFoundException, PathNotInRootException,
    TransferNotAllowedException
)


class Task(ABC):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        self.validate(protocol, auth, local_path, remote_path)

        self._protocol = protocol
        self._auth = auth
        self._local_path = local_path
        self._remote_path = remote_path
        self._uid: UUID = uuid4()

        self._status: Status = Status.QUEUED
        self._files: list[FileTransfer] = self.get_files_for_task()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Status:
            raise ValueError('Status must be: queued, downloading, \
                             interrupted or complete')
        self._status = value

    @property
    def uid(self):
        return self._uid

    @abstractmethod
    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        pass

    @staticmethod
    def check_if_local_path_exists(local_path: Path) -> None:
        if not local_path.exists():
            raise PathNotFoundException('The local path does not exists')

    @staticmethod
    def check_if_local_path_in_root(local_path: Path) -> None:
        if local_path not in Path(config['paths']['root']):
            raise PathNotInRootException('The local path is not in root')

    @staticmethod
    def check_if_remote_path_available(protocol: TransferProtocol, auth: Auth,
                                       remote_path: str) -> None:
        if protocol is TransferProtocol.HTTP:
            HTTPTransfer.check_if_remote_available(remote_path, auth)
        else:
            S3Transfer.check_if_remote_available(remote_path, auth)

    @abstractmethod
    def get_files_for_task(self) -> list[FileTransfer]:
        pass


class DownloadTask(Task):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        super().__init__(protocol, auth, local_path, remote_path)

    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        self.check_if_local_path_exists(local_path)
        self.check_if_local_path_in_root(local_path)
        self.check_if_remote_path_available(protocol, auth, remote_path)

    def get_files_for_task(self) -> list[FileTransfer]:
        glob = self._local_path.glob('**/*')
        local_paths = [path for path in glob if path.is_file()]
        remote_paths = [self._remote_path + '/' +
                        str(path.relative_to(self._local_path))
                        for path in local_paths]
        return [FileTransfer(local_path, remote_path)
                for local_path, remote_path
                in zip(local_paths, remote_paths)]


class UploadTask(Task):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        super().__init__(protocol, auth, local_path, remote_path)

    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        self.check_if_local_path_exists(local_path)
        self.check_if_local_path_in_root(local_path)
        self.check_if_transfer_is_allowable(protocol)
        self.check_if_remote_path_available(protocol, auth, remote_path)

    @staticmethod
    def check_if_transfer_is_allowable(protocol: TransferProtocol) -> None:
        if protocol is TransferProtocol.HTTP:
            raise TransferNotAllowedException('Can not upload via HTTP')

    def get_files_for_task(self) -> list[FileTransfer]:
        if self._protocol is TransferProtocol.HTTP:
            return [FileTransfer(self._local_path, self._remote_path)]
        if self._protocol is TransferProtocol.S3:
            ...
            return []