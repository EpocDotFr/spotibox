class UserNotFoundException(Exception):
    pass


class UnauthenticatedWithSpotifyException(Exception):
    pass


class BaseExceptionWithUser(Exception):
    def __init__(self, user):
        self.user = user

        super().__init__()


class NoSpotifyDeviceException(BaseExceptionWithUser):
    pass


class PasswordRequiredException(BaseExceptionWithUser):
    pass
