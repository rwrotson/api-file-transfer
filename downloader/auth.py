from dataclasses import dataclass
from base64 import b64encode

from downloader.enums import AuthMode


@dataclass
class Auth:
    mode: AuthMode
    data: dict[str, str]

    def get_key(self) -> dict[str, str]:
        match self.mode:
            case AuthMode.NONE:
                return {}

            case AuthMode.BASIC:
                user, password = self.data.values()
                encoded_str = b64encode(
                    bytes(f'{user}:{password}', 'utf-8')
                ).decode('utf-8')
                return {'Authorization': f'Basic {encoded_str}'}

            case AuthMode.TOKEN:
                token = self.data.values()
                return {'Authorization': f'Bearer {token}'}

            case AuthMode.S3:
                return
