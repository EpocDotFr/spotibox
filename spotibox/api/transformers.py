from collections import OrderedDict
from flask_restful import fields

track = OrderedDict([
    ('id', fields.String),
    ('title', fields.String(attribute='name')),
    ('artist_name', fields.String(attribute='artists.0.name')), # TODO Concatenate all artists
    ('album_cover_small', fields.String(attribute='images.0.url')), # TODO Take the smallest
    ('album_cover_medium', fields.String(attribute='images.0.url')), # TODO Take the medium
])
