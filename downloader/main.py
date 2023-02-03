import uvicorn

from downloader.urls import app


def main():
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')


if __name__ == "__main__":
    main()