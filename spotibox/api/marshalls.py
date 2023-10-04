from collections import OrderedDict
from flask_restful import fields


class Action(fields.Raw):
    def format(self, value):
        if isinstance(value, bool):
            return not value

        return True


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

playback_state = OrderedDict([
    ('can_pause', Action(attribute='player.actions.disallows.pausing', default=True)),
    ('can_start_or_resume', Action(attribute='player.actions.disallows.resuming', default=True)),
    ('can_skip_to_next', Action(attribute='player.actions.disallows.skipping_next', default=True)),
    ('can_skip_to_previous', Action(attribute='player.actions.disallows.skipping_prev', default=True)),
    ('now_playing', fields.Nested(track, attribute='player.item', allow_null=True, default=None)),
    ('queue', fields.List(fields.Nested(track), attribute='queue', default=[])),
])
