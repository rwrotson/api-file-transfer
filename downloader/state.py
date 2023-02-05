from pathlib import Path
from uuid import uuid4, UUID
from queue import Queue
from dataclasses import dataclass
from abc import ABC, abstractmethod

from downloader.schemas import Auth
from downloader.config import config
from downloader.enums import (
    StatusInQueue, Status,
    TransferDirection, TransferProtocol
)
from downloader.exceptions import (
    PathNotFoundException, PathNotInRootException,
    TransferNotAllowedException
)


@dataclass
class File:
    direction: TransferDirection
    protocol: TransferProtocol
    local_path: Path
    remote_path: Path
    status: Status = Status.QUEUED


class Task:
    def __init__(self, direction: TransferDirection,
                 protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:

        self.validate(direction, protocol, local_path, remote_path)

        self.direction = direction
        self.protocol = protocol
        self.auth = auth
        self.local_path = local_path
        self.remote_path = remote_path
        self.uid: UUID = uuid4()

        self.status: StatusInQueue = StatusInQueue.QUEUED
        self.files: list[File] = self.get_files_for_task()

    def validate(self, direction: TransferDirection,
                 protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        self.check_if_local_path_exists(local_path)
        self.check_if_local_path_in_root(local_path)
        self.check_if_transfer_is_allowable(direction, protocol)
        self.check_if_remote_path_available(protocol, auth, remote_path)

    @staticmethod
    def check_if_local_path_exists(local_path: Path) -> None:
        if not local_path.exists():
            raise PathNotFoundException('The local path does not exists')

    @staticmethod
    def check_if_local_path_in_root(local_path: Path) -> None:
        if local_path not in Path(config['paths']['root']):
            raise PathNotInRootException('The local path is not in root')

    @staticmethod
    def check_if_transfer_is_allowable(direction: TransferDirection,
                                       protocol: TransferProtocol) -> None:
        if (direction is TransferDirection.UPLOAD and
                protocol is TransferProtocol.HTTP):
            raise TransferNotAllowedException('Can not upload via HTTP')

    @staticmethod
    def check_if_remote_path_available(protocol: TransferProtocol,
                                       auth: Auth, remote_path: Path) -> None:
        pass

    def get_files_for_task(self) -> list[File]:
        pass


class TaskAbstract(ABC):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        self.validate(protocol, auth, local_path, remote_path)

        self._protocol = protocol
        self._auth = auth
        self._local_path = local_path
        self._remote_path = remote_path
        self._uid: UUID = uuid4()

        self._status: StatusInQueue = StatusInQueue.QUEUED
        self._files: list[File] = self.get_files_for_task()

    @abstractmethod
    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
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
    def check_if_remote_path_available(protocol: TransferProtocol,
                                       auth: Auth, remote_path: Path) -> None:
        pass

    @abstractmethod
    def get_files_for_task(self) -> list[File]:
        pass

    @abstractmethod
    def initiate(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def get_status(self):
        pass


class DownloadTask(TaskAbstract):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        super().__init__(protocol, auth, local_path, remote_path)

    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        self.check_if_local_path_exists(local_path)
        self.check_if_local_path_in_root(local_path)
        self.check_if_remote_path_available(protocol, auth, remote_path)

    def get_files_for_task(self) -> list[File]:
        pass


class UploadTask(TaskAbstract):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        self.validate(protocol, auth, local_path, remote_path)
        super().__init__(protocol, auth, local_path, remote_path)

    def validate(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: Path) -> None:
        self.check_if_local_path_exists(local_path)
        self.check_if_local_path_in_root(local_path)
        self.check_if_transfer_is_allowable(protocol)
        self.check_if_remote_path_available(protocol, auth, remote_path)

    @staticmethod
    def check_if_transfer_is_allowable(protocol: TransferProtocol) -> None:
        if protocol is TransferProtocol.HTTP:
            raise TransferNotAllowedException('Can not upload via HTTP')

    def get_files_for_task(self) -> list[File]:
        pass


class AppState:
    def __init__(self):
        self.tasks_queue = Queue()
        self.files_queue = Queue(
            maxsize=config['transfer_settings']['files_limit']
        )
        self.completed_files: list[File] = []
        self.stopped_files: list[File] = []
