from flask_restful import reqparse, inputs

get_room_catalog = reqparse.RequestParser()
get_room_catalog.add_argument('q', location='args', required=True)

put_room_playback_volume = reqparse.RequestParser()
put_room_playback_volume.add_argument('volume', location='json', required=True, type=inputs.int_range(0, 100))

put_room_queue = reqparse.RequestParser()
put_room_queue.add_argument('track_id', location='json', required=True)
