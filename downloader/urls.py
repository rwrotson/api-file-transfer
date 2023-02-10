from typing import Optional
from uuid import UUID
from pathlib import Path
from pydantic import AnyHttpUrl
from fastapi import FastAPI

from downloader.enums import TransferProtocol
from downloader.auth import Auth
from downloader.schemas import TransferQuery
from downloader.state import UploadTask, DownloadTask, get_app_state


app = FastAPI()


@app.post('/upload')
async def upload_files(query: TransferQuery):
    try:
        new_task = UploadTask(
            protocol=TransferProtocol(query.protocol),
            auth=Auth(**query.auth),
            local_path=Path(query.source),
            remote_path=query.destination
        )
    except Exception as e:
        return  # e.to_json
    app_state = get_app_state()
    app_state.add_task(new_task)
    return new_task.uid


@app.post('/download')
async def download_files(query: TransferQuery):
    try:
        new_task = DownloadTask(
            protocol=TransferProtocol(query.protocol),
            auth=Auth(**query.auth),
            local_path=Path(query.source),
            remote_path=AnyHttpUrl(query.destination)
        )
    except Exception:
        return 'Error'
    app_state = get_app_state()
    app_state.add_task(new_task)
    return new_task.uid


@app.post('/cancel')
async def cancel_transfer(uid: UUID):
    app_state = get_app_state()
    app_state.cancel_task(uid)


@app.get('/status')
async def get_status(uid: UUID, path: Optional[str]):
    app_state = get_app_state()
    if path is None:
        return app_state.get_task_status()
    return app_state.get_file_status()
