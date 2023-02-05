from uuid import UUID
from pathlib import Path
from fastapi import FastAPI

from downloader.enums import TransferDirection, TransferProtocol
from downloader.schemas import TransferQuery, StatusQuery, Auth
from downloader.state import Task

app = FastAPI()


@app.post('/upload')
def upload_files(query: TransferQuery):
    try:
        new_task = Task(
            direction=TransferDirection.UPLOAD,
            protocol=TransferProtocol(query.protocol),
            auth=Auth(**query.auth),
            local_path=Path(query.source),
            remote_path=Path(query.destination)
        )
    except Exception:
        return 'Error'
    ...
    return Task.uid


@app.post('/download')
def download_files(query: TransferQuery):
    try:
        new_task = Task(
            direction=TransferDirection.UPLOAD,
            protocol=TransferProtocol(query.protocol),
            auth=Auth(**query.auth),
            local_path=Path(query.source),
            remote_path=Path(query.destination)
        )
    except Exception:
        return 'Error'
    ...
    return Task.uid


@app.post('/cancel')
def cancel_transfer(uid: UUID):
    pass


@app.get('/status')
def get_status(query: StatusQuery):
    pass
