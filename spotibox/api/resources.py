from flask_restful import Resource, marshal_with
import spotibox.api.transformers as transformers
import spotibox.api.validators as validators


class RoomCatalogResource(Resource):
    @marshal_with(transformers.track)
    def get(self, room_name: str):
        """Search Spotify catalog"""
        args = validators.get_room_catalog.parse_args()


class RoomPlaybackResource(Resource):
    def put(self, room_name: str):
        """Start or resume playback"""
        pass

    def delete(self, room_name: str):
        """Pause playback"""
        pass


class RoomPlaybackVolumeResource(Resource):
    def put(self, room_name: str):
        """Set playback volume"""
        pass


class RoomQueueResource(Resource):
    def delete(self, room_name: str):
        """Skip to previous track"""
        pass

    def post(self, room_name: str):
        """Skip to next track"""
        pass

    def patch(self, room_name: str):
        """Add track to queue"""
        pass
