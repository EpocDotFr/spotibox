from spotibox.exceptions import UserNotFoundException, InactiveRoomException
from flask_restful import Resource, marshal_with, abort
from spotibox.models import User
import spotibox.api.marshalls as marshalls
import spotibox.api.validators as validators


def fetch_user(spotify_id: str) -> User:
    try:
        return User.get_by_spotify_id(spotify_id)
    except UserNotFoundException:
        abort(404, message='This room does not exist.')
    except InactiveRoomException:
        abort(412, message='This room is inactive.')


class RoomCatalogResource(Resource):
    @marshal_with(marshalls.track)
    def get(self, spotify_id: str):
        """Search Spotify catalog"""
        args = validators.get_room_catalog.parse_args()
        user = fetch_user(spotify_id)

        return user.create_spotify_api_client().search(args.q, limit=20, offset=0, type='track')['tracks']['items']


class RoomPlaybackResource(Resource):
    def put(self, spotify_id: str):
        """Start or resume playback"""
        user = fetch_user(spotify_id)

        user.create_spotify_api_client().start_playback()

        return '', 204

    def delete(self, spotify_id: str):
        """Pause playback"""
        user = fetch_user(spotify_id)

        user.create_spotify_api_client().pause_playback()

        return '', 204


class RoomPlaybackVolumeResource(Resource):
    def put(self, spotify_id: str):
        """Set playback volume"""
        args = validators.put_room_playback_volume.parse_args()
        user = fetch_user(spotify_id)

        user.create_spotify_api_client().volume(args.volume)

        return '', 204


class RoomQueueResource(Resource):
    def delete(self, spotify_id: str):
        """Skip to previous track"""
        pass

    def patch(self, spotify_id: str):
        """Skip to next track"""
        pass

    def post(self, spotify_id: str):
        """Add track to queue"""
        pass
