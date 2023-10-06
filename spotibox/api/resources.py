from spotibox.exceptions import UserNotFoundException, UnauthenticatedWithSpotifyException, NoSpotifyDeviceException
from flask_restful import Resource, marshal_with, abort
from spotipy import SpotifyException
from spotibox.models import User
from app import cache
import spotibox.api.marshalls as marshalls
import spotibox.api.validators as validators


def fetch_user(spotify_id: str) -> User:
    inactive_message = 'This room is inactive.'

    try:
        return User.get_by_spotify_id(spotify_id)
    except UserNotFoundException:
        abort(404, message='This room does not exist.')
    except UnauthenticatedWithSpotifyException:
        abort(412, message=inactive_message)
    except NoSpotifyDeviceException as e:
        if e.user.is_current_user_room_owner:
            message = 'Your are the host of this room: please open Spotify on any device of your like.'
        else:
            message = inactive_message

        abort(412, message=message)


class RoomCatalogResource(Resource):
    @marshal_with(marshalls.track)
    def get(self, spotify_id: str):
        """Search Spotify catalog"""
        try:
            user = fetch_user(spotify_id)
            args = validators.get_room_catalog.parse_args()

            return user.create_spotify_api_client().search(args.q, limit=20, offset=0, type='track')['tracks']['items']
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')


class RoomPlaybackResource(Resource):
    def put(self, spotify_id: str):
        """Start or resume playback"""
        try:
            user = fetch_user(spotify_id)

            user.create_spotify_api_client().start_playback()

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')

    def delete(self, spotify_id: str):
        """Pause playback"""
        try:
            user = fetch_user(spotify_id)

            user.create_spotify_api_client().pause_playback()

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')

    def patch(self, spotify_id: str):
        """Skip to previous track"""
        try:
            user = fetch_user(spotify_id)

            user.create_spotify_api_client().previous_track()

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')

    def post(self, spotify_id: str):
        """Skip to next track"""
        try:
            user = fetch_user(spotify_id)

            user.create_spotify_api_client().next_track()

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')


class RoomPlaybackStateResource(Resource):
    @marshal_with(marshalls.playback_state)
    @cache.cached(timeout=3)
    def get(self, spotify_id: str):
        """Get playback state"""
        try:
            user = fetch_user(spotify_id)

            return {
                # TODO Check if currently_playing_type == 'track'
                'playback': user.create_spotify_api_client().current_playback(),
                'queue': [
                    item for item in user.create_spotify_api_client().queue()['queue'] if item['type'] == 'track'
                ]
            }
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')


class RoomPlaybackVolumeResource(Resource):
    def put(self, spotify_id: str):
        """Set playback volume"""
        try:
            user = fetch_user(spotify_id)
            args = validators.put_room_playback_volume.parse_args()

            user.create_spotify_api_client().volume(args.volume)

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')


class RoomPlaybackPositionResource(Resource):
    def put(self, spotify_id: str):
        """Seek to position"""
        try:
            user = fetch_user(spotify_id)
            args = validators.put_room_playback_position.parse_args()

            user.create_spotify_api_client().seek_track(args.position)

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')


class RoomQueueResource(Resource):
    def post(self, spotify_id: str):
        """Add track to queue"""
        try:
            user = fetch_user(spotify_id)
            args = validators.put_room_queue.parse_args()

            user.create_spotify_api_client().add_to_queue(args.track_id)

            return {}, 202
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')
