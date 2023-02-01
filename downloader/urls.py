from fastapi import FastAPI
from downloader.schemas import TransferQuery

app = FastAPI()


@app.post('/upload')
def upload_files(query: TransferQuery):

    return query.uid


@app.post('/download')
def download_files(query: TransferQuery):
    pass


@app.post('/cancel?uid=<uid>')
def cancel_transfer():
    pass


@app.get('/status?uid=<uid>&path=<path>')
def get_status():
    pass
