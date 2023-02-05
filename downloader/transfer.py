from abc import ABC, abstractmethod


class Transfer(ABC):
    @abstractmethod
    def check_if_remote_available(self):
        # ???
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def upload(self):
        pass


class HTTPTransfer(Transfer):
    def download(self):
        pass

    def upload(self):
        pass


class S3Transfer(Transfer):
    def download(self):
        pass

    def upload(self):
        pass
