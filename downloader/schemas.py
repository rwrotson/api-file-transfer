from dataclasses import dataclass
from pydantic import BaseModel, ValidationError, validator

from downloader.enums import TransferProtocol, AuthMode, Status


class TransferQuery(BaseModel):
    source: str
    destination: str
    protocol: str
    auth: dict[str, str | dict[str, str]]

    @classmethod
    @validator('protocol')
    def must_be_http_or_s3(cls, protocol):
        if protocol not in TransferProtocol:
            raise ValidationError('Protocol must be HTTP or S3')
        return protocol

    @classmethod
    @validator('auth')
    def must_be_in_correct_format(cls, auth):
        if auth.get('mode') is None:
            raise ValidationError('Auth must contain mode field')
        if auth.get('data') is None:
            raise ValidationError('Auth must contain data field')
        if auth['mode'] not in AuthMode:
            raise ValidationError('Mode must be one of: BASIC, TOKEN or S3')
        return auth


class InProgressData(BaseModel):
    size: int
    completed: int


@dataclass
class ErrorData:
    message: str | None


class StatusResponse(BaseModel):
    status: Status
    data: InProgressData | ErrorData
