from abc import ABC


class Downloader(ABC):
    pass


class HTTPDownloader(Downloader):
    pass


class S3Downloader(Downloader):
    pass
