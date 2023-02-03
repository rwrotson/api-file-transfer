class PathNotFoundException(Exception):
    """Raised when there is no such path in source"""
    pass


class PathNotInRootException(Exception):
    """Raised when trying to reach paths outside root"""
    pass


class AuthentificationException(Exception):
    """Raised when authentification token is not correct"""
    pass


class ConnectionException(Exception):
    """Raised when the network connection is lost"""
    pass
