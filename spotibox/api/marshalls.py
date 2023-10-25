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


class RemainingField(DurationField):
    def format(self, value):
        return '-' + super().format(value)


class SmallestAlbumCoverField(fields.String):
    def format(self, value):
        album_covers = sorted(value, key=lambda i: i['height'])

        return album_covers[0]['url']


class ArtistsField(fields.String):
    def format(self, value):
        return ', '.join(
            [artist['name'] for artist in value]
        )

track = OrderedDict([
    ('id', fields.String),
    ('title', fields.String(attribute='name')),
    ('duration_text', DurationField(attribute='duration_ms')),
    ('duration_ms', fields.Integer(attribute='duration_ms')),
    ('artist_name', ArtistsField(attribute='artists')),
    ('album_cover', SmallestAlbumCoverField(attribute='album.images')),
])

playback_state = OrderedDict([
    ('can_pause', ActionField(attribute='playback.actions.disallows.pausing', default=True)),
    ('can_start_or_resume', ActionField(attribute='playback.actions.disallows.resuming', default=True)),
    ('can_skip_to_next', ActionField(attribute='playback.actions.disallows.skipping_next', default=True)),
    ('can_skip_to_previous', ActionField(attribute='playback.actions.disallows.skipping_prev', default=True)),
    ('volume', fields.Integer(attribute='playback.device.volume_percent', default=0)),
    ('now_playing', fields.Nested(track, attribute='playback.item', allow_null=True, default=None)),
    ('remaining_text', RemainingField(attribute='playback.remaining_ms', default='')),
    ('progress_text', DurationField(attribute='playback.progress_ms', default='')),
    ('progress_ms', fields.Integer(attribute='playback.progress_ms', default=0)),
    ('total_text', DurationField(attribute='queue.total_ms', default='')),
    ('queue', fields.List(fields.Nested(track), attribute='queue.items', default=[])),
])
