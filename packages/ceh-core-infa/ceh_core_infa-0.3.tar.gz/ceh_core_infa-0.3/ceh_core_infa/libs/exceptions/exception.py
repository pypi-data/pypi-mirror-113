class ConnectionApiError(Exception):
    pass


class NotValidStatusCode(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class NumberAttemptsOver(Exception):
    pass


class ResourceStateException(Exception):
    pass


class SomeVersionException(Exception):
    pass


class ParamsNotFoundException(Exception):
    pass


class ResourceBlockedException(Exception):
    pass


class ResourceLockedException(Exception):
    pass
