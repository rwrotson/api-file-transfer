from uuid import UUID
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from pydantic import BaseModel


class TransferProtocol(Enum):
    HTTP = auto()
    S3 = auto()


class TransferQuery(BaseModel):
    source: Path
    destination: Path
    protocol: TransferProtocol
    uid: UUID


class Status(Enum):
    QUEUED = auto()
    DOWNLOADING = auto()
    INTERRUPTED = auto()
    COMPLETE = auto()


@dataclass
class InProgressData:
    done: int
    total: int


class ErrorData:
    message: str | None


class StatusResponse(BaseModel):
    status: Status
    data: InProgressData | ErrorData

