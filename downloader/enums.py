from enum import StrEnum, EnumMeta, auto


class EnumWithContains(EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class TransferDirection(StrEnum, metaclass=EnumWithContains):
    UPLOAD = auto()
    DOWNLOAD = auto()


# 'upload' -> TransferDirection.UPLOAD
a = TransferDirection('upload')
print(type(a), a)


class TransferProtocol(StrEnum):
    HTTP = auto()
    S3 = auto()


class AuthMode(StrEnum):
    BASIC = auto()
    TOKEN = auto()
    S3 = auto()


class StatusInQueue(StrEnum):
    QUEUED = auto()
    DOWNLOADING = auto()


class Status(StrEnum):
    QUEUED = auto()
    DOWNLOADING = auto()
    INTERRUPTED = auto()
    COMPLETE = auto()
