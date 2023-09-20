(function() {
    'use strict';

    window.Spotibox = {
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
        },

        generateRandomString(length) {
            let text = '';
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-~';

            for (let i = 0; i < length; i++) {
                text += chars.charAt(Math.floor(Math.random() * chars.length));
            }

            return text;
        },

        base64encode(string) {
            return btoa(String.fromCharCode.apply(null, new Uint8Array(string)))
                .replace(/\+/g, '-')
                .replace(/\//g, '_')
                .replace(/=+$/, '');
        }
    };
})();