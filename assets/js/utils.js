(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Utils = {
        transformTracks(tracks) {
            return tracks.map(function (track) {
                return {
                    id: track.id,
                    title: track.title,
                    artist_name: track.artist.name,
                    album_cover_small: track.album.cover_small,
                    album_cover_medium: track.album.cover_medium
                };
            });
        },

        isFirst(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === 0;
            }

            return false;
        },

        isLast(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === array.length - 1;
            }

            return false;
        },

        isEmpty(array) {
            return array.length === 0;
        },

        move(array, item, direction) {
            const index = array.indexOf(item);
            const newIndex = direction === 'up' ? index - 1 : index + 1;

            if (index > -1 && newIndex >= 0 && newIndex <= array.length) {
                array.splice(index, 1);
                array.splice(newIndex , 0, item);
            }
        },};
})();