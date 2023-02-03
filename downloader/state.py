from pathlib import Path
from uuid import uuid4, UUID
from queue import Queue

from downloader.config import config
from downloader.enums import StatusInQueue, Status, TransferDirection, TransferProtocol


class File:
    def __init__(self, direction: TransferDirection,
                 protocol: TransferProtocol,
                 source: Path, destination: Path) -> None:
        self.direction = direction
        self.protocol = protocol
        self.source = source
        self.destination = destination
        self.status: Status = Status.QUEUED


class Task:
    def __init__(self, direction: TransferDirection,
                 protocol: TransferProtocol,
                 source: Path, destination: Path) -> None:
        self.validate(direction, protocol, source, destination)

        self.direction = direction
        self.protocol = protocol
        self.source = source
        self.destination = destination
        self.uid: UUID = uuid4()

        self.status: StatusInQueue = StatusInQueue.QUEUED
        self.files: list[File] = self.get_files_for_task()

    def validate(self, direction: TransferDirection,
                 protocol: TransferProtocol,
                 source: Path, destination: Path) -> None:
        self.check_if_source_exists(direction, protocol, source, destination)

    @staticmethod
    def check_if_source_exists(direction: TransferDirection,
                               protocol: TransferProtocol,
                               source: Path, destination: Path) -> None:
        if direction is TransferDirection.UPLOAD:
        raise

    @staticmethod
    def check_if_destination_exists():
        pass


    def get_files_for_task(self) -> list[File]:
        pass


class AppState:
    def __init__(self):
        self.tasks_queue = Queue()
        self.files_queue = Queue(
            maxsize=config['transfer_settings']['files_limit']
        )
        self.completed_files_paths: list[Path] = []
        self.stopped_files_paths: list[Path] = []


