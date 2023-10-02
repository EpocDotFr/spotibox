class UserNotFoundException(Exception):
    pass


class UnauthenticatedWithSpotifyException(Exception):
    pass


class NoSpotifyDeviceException(Exception):
    def __init__(self, user):
        self.user = user

        super().__init__()
