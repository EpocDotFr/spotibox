from collections import OrderedDict
from flask_restful import fields


def artists_name(track) -> str:
    return ', '.join(
        [artist['name'] for artist in track['artists']]
    )


def album_cover_small(track) -> str:
    album_covers = sorted(track['album']['images'], key=lambda i: i['height'])

    return album_covers[0]['url']


def album_cover_large(track) -> str:
    album_covers = sorted(track['album']['images'], key=lambda i: i['height'])

    try:
        return album_covers[1]['url']
    except IndexError:
        return album_covers[0]['url']


track = OrderedDict([
    ('id', fields.String),
    ('title', fields.String(attribute='name')),
    ('artist_name', fields.String(attribute=artists_name)),
    ('album_cover_small', fields.String(attribute=album_cover_small)),
    ('album_cover_large', fields.String(attribute=album_cover_large)),
])
