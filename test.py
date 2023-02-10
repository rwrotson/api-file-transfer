from pathlib import Path
import asyncio

from downloader.auth import Auth
from downloader.state import FileTransfer
from downloader.transfer import HTTPTransfer
from downloader.enums import AuthMode


TEST_HTTP = 'https://med.stanford.edu/news/all-news/2021/09/cat-fur-color-patterns/_jcr_content/main/image.img.780.high.jpg/cat_by-Kateryna-T-Unsplash.jpg'

fl = FileTransfer(
    local_path=Path('face_landmarks.dat.bz2'),
    remote_path=TEST_HTTP,
    auth=Auth(AuthMode.NONE, {})
)
transfer = HTTPTransfer(fl)
asyncio.run(transfer.download())
