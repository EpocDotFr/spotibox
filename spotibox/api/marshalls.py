from collections import OrderedDict
from flask_restful import fields


class ActionField(fields.Boolean):
    def format(self, value):
        if isinstance(value, bool):
            return not value

        return True


class DurationField(fields.String):
    def format(self, value):
        if not isinstance(value, int):
            return ''

        minutes, seconds = divmod(value / 1000, 60)

        return f'{minutes:02.0f}:{seconds:02.0f}'


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
    ('duration_text', DurationField(attribute='duration_ms')),
    ('duration_ms', fields.Integer(attribute='duration_ms')),
    ('artist_name', fields.String(attribute=artists_name)),
    ('album_cover_small', fields.String(attribute=album_cover_small)),
    ('album_cover_large', fields.String(attribute=album_cover_large)),
])

playback_state = OrderedDict([
    ('can_pause', ActionField(attribute='playback.actions.disallows.pausing', default=True)),
    ('can_start_or_resume', ActionField(attribute='playback.actions.disallows.resuming', default=True)),
    ('can_skip_to_next', ActionField(attribute='playback.actions.disallows.skipping_next', default=True)),
    ('can_skip_to_previous', ActionField(attribute='playback.actions.disallows.skipping_prev', default=True)),
    ('volume', fields.Integer(attribute='playback.device.volume_percent', default=0)),
    ('now_playing', fields.Nested(track, attribute='playback.item', allow_null=True, default=None)),
    ('progress_text', DurationField(attribute='playback.progress_ms', default='')),
    ('progress_ms', fields.Integer(attribute='playback.progress_ms', default=0)),
    ('queue', fields.List(fields.Nested(track), attribute='queue', default=[])),
])
