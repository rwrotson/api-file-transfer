class PathNotFoundException(Exception):
    """Raised when there is no such path in source"""
    pass


class PathNotInRootException(Exception):
    """Raised when trying to reach paths outside root"""
    pass


class TransferNotAllowedException(Exception):
    """Raised when the transfer is not possible by design"""
    pass


class RemotePathNotAvailable(Exception):
    """Raised when the remote endpoint is not available"""
    pass


class AuthentificationException(Exception):
    """Raised when authentification token is not correct"""
    pass


class ConnectionException(Exception):
    """Raised when the network connection is lost"""
    pass
