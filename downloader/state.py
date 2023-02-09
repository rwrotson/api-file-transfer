from pathlib import Path
from uuid import uuid4, UUID
from queue import Queue
from dataclasses import dataclass
from abc import ABC, abstractmethod

from downloader.transfer import HTTPTransfer, S3Transfer
from downloader.schemas import Auth
from downloader.config import config
from downloader.enums import (Status, TransferProtocol)
from downloader.exceptions import (
    PathNotFoundException, PathNotInRootException,
    TransferNotAllowedException
)


@dataclass
class File:
    local_path: Path
    remote_path: str
    auth: Auth = None
    status: Status = Status.QUEUED


class Task(ABC):
    def __init__(self, protocol: TransferProtocol, auth: Auth,
                 local_path: Path, remote_path: str) -> None:
        self.validate(protocol, auth, local_path, remote_path) # separate class?

        self._protocol = protocol
        self._auth = auth
        self._local_path = local_path
        self._remote_path = remote_path
        self._uid: UUID = uuid4()

        self._status: Status = Status.QUEUED
        self._files: list[File] = self.get_files_for_task()

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
    def get_files_for_task(self) -> list[File]:
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

    def get_files_for_task(self) -> list[File]:
        glob = self._local_path.glob('**/*')
        local_paths = [path for path in glob if path.is_file()]
        remote_paths = [self._remote_path + '/' +
                        str(path.relative_to(self._local_path))
                        for path in local_paths]
        return [File(local_path, remote_path)
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

    def get_files_for_task(self) -> list[File]:
        if self._protocol is TransferProtocol.HTTP:
            return [File(self._local_path, self._remote_path)]

        if self._protocol is TransferProtocol.S3:
            ...
            return []


class AppState:
    def __init__(self):
        self._tasks_queue = Queue()
        self._completed_tasks: list[Task] = []

        self._files_queue = Queue(
            maxsize=config['transfer_settings']['files_limit']
        )
        self._completed_files: list[File] = []
        self._stopped_files: list[File] = []

    def add_task(self, task: Task):
        pass

    def delete_task(self, uid: UUID):
        # ?
        pass

    def add_file_to_queue(self, file: File):
        pass

    def add_file_to_completed_file(self, file: File):
        pass

    def add_file_to_stopped_file(self, file: File):
        pass

    def is_file_already_added(self, file: File):
        if


def get_app_state() -> AppState:
    if not hasattr(get_app_state, 'instances'):
        get_app_state._instances = dict()
    ...
