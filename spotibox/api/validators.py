from flask_restful import reqparse, inputs

get_room_catalog = reqparse.RequestParser()
get_room_catalog.add_argument('q', location='args', required=True)
