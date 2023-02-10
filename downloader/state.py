from pathlib import Path
from uuid import UUID
from queue import Queue

from downloader.tasks import Task
from downloader.transfer import FileTransfer
from downloader.config import config


class AppState:
    def __init__(self):
        self._tasks_queue = Queue()
        self._completed_tasks: list[Task] = []

        self._files_queue = Queue(
            maxsize=config['transfer_settings']['files_limit']
        )
        self._completed_files: list[FileTransfer] = []
        self._stopped_files: list[FileTransfer] = []

    def add_task(self, task: Task):
        pass

    def cancel_task(self, uid: UUID):
        pass

    def get_task_status(self, uid: UUID):
        pass

    def get_file_status(self, uid: UUID, path: Path):
        pass

    def add_file_to_queue(self, file: FileTransfer):
        pass

    def add_file_to_completed_files(self, file: FileTransfer):
        pass

    def add_file_to_stopped_files(self, file: FileTransfer):
        pass

    def is_file_already_added(self, file: FileTransfer):
        pass


def get_app_state() -> AppState:
    if not hasattr(get_app_state, 'instances'):
        get_app_state._instances = dict()
    return
