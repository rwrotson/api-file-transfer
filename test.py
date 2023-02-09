from pathlib import Path
import asyncio
import aiohttp

from downloader.state import File
from downloader.transfer import HTTPTransfer

TEST_CAT = 'https://med.stanford.edu/news/all-news/2021/09/cat-fur-color-patterns/_jcr_content/main/image.img.780.high.jpg/cat_by-Kateryna-T-Unsplash.jpg'
TEST_HTTP = 'https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt'
TEST2 = 'https://drive.google.com/file/d/1DD5H1cqB9VitfbnVu7KU7uPIANCzIzts'


fl = File(Path('/Users/igorlashkov/Pictures/pic2.jpg'), TEST_CAT)
transfer = HTTPTransfer(fl)
asyncio.run(transfer.download_file())