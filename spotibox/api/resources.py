from flask_restful import Resource, marshal_with, abort
from spotipy import SpotifyException
from spotibox.models import User
from typing import Dict
from app import cache
import spotibox.api.validators as validators
import spotibox.api.marshalls as marshalls
import spotibox.exceptions as exceptions


def fetch_user(spotify_id: str) -> User:
    try:
        return User.get_by_spotify_id(spotify_id)
    except exceptions.UserNotFoundException:
        abort(404, message='This room does not or no longer exist.')
    except exceptions.UnauthenticatedWithSpotifyException:
        abort(412, message='This room is inactive.')
    except exceptions.PasswordRequiredException:
        abort(401, message='This room is private, please reload the page to submit a password.')


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
    def get(self, spotify_id: str):
        """Get playback state"""
        try:
            user = fetch_user(spotify_id)

            return self._fetch_and_cache_playback_state(user)
        except SpotifyException as e:
            abort(502, message=f'Spotify error: {e.reason} ({e.http_status})')

    @cache.memoize(timeout=3)
    def _fetch_and_cache_playback_state(self, user: User) -> Dict:
        playback = user.create_spotify_api_client().current_playback()

        try:
            playback['remaining_ms'] = playback['item']['duration_ms'] - playback['progress_ms']
        except IndexError:
            pass

        queue_items = [
            item for item in user.create_spotify_api_client().queue()['queue'] if item['type'] == 'track'
        ]

        queue_total_ms = sum([
            track['duration_ms'] for track in queue_items
        ])

        return {
            'playback': playback, # TODO Check if currently_playing_type == 'track'
            'queue': {
                'items': queue_items,
                'total_ms': queue_total_ms
            }
        }

    def __repr__(self):
        return f'RoomPlaybackStateResource'


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
