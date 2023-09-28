from flask_restful import Resource, marshal_with
import spotibox.api.transformers as transformers
import spotibox.api.validators as validators


class RoomCatalogResource(Resource):
    @marshal_with(transformers.track)
    def get(self, spotify_id: str):
        """Search Spotify catalog"""
        args = validators.get_room_catalog.parse_args()


class RoomPlaybackResource(Resource):
    def put(self, spotify_id: str):
        """Start or resume playback"""
        pass

    def delete(self, spotify_id: str):
        """Pause playback"""
        pass


class RoomPlaybackVolumeResource(Resource):
    def put(self, spotify_id: str):
        """Set playback volume"""
        pass


class RoomQueueResource(Resource):
    def delete(self, spotify_id: str):
        """Skip to previous track"""
        pass

    def post(self, spotify_id: str):
        """Skip to next track"""
        pass

    def patch(self, spotify_id: str):
        """Add track to queue"""
        pass
