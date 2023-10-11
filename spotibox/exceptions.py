class UserNotFoundException(Exception):
    pass


class UnauthenticatedWithSpotifyException(Exception):
    pass


class BaseExceptionWithUser(Exception):
    def __init__(self, user):
        self.user = user

        super().__init__()


class PasswordRequiredException(BaseExceptionWithUser):
    pass
