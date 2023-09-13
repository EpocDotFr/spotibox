(function() {
    'use strict';

    class Deezbox {
        pusherKey = '54c230647abc0f6ac73d';
        pusherCluster = 'eu';

        deezerAppId = '632324';

        constructor() {
            /*this.pusher = new Pusher(this.pusherKey, {
              cluster: this.pusherCluster
            });

            this.pusherChannel = this.pusher.subscribe('room');*/

            Alpine.store('playlist', {
                tracks: [],
                queue: function (track) {
                    this.tracks.push(Object.assign({}, track));
                },
                remove: function (track) {
                    const index = this.tracks.indexOf(track);

                    if (index > -1) {
                        this.tracks.splice(index, 1);
                    }
                },
                clear: function () {
                    this.tracks = [];
                },
                moveUp(track) {

                },
                moveDown(track) {

                },
                isFirst(track) {
                    return Deezbox.isFirst(this.tracks, track);
                },
                isLast(track) {
                    return Deezbox.isLast(this.tracks, track);
                },
                isEmpty() {
                    return Deezbox.isEmpty(this.tracks);
                }
            });

            Alpine.store('nowPlaying', {});

            DZ.init({
                appId: this.deezerAppId,
                channelUrl: `${window.location.origin}/channel.html?`,
                player: {
                    onload: function (player) {
                        console.log(player);
                    }
                }
            });
        }

        static transformTracks(tracks) {
            return tracks.map(function (track) {
                return {
                    id: track.id,
                    title: track.title,
                    artist_name: track.artist.name,
                    album_cover_small: track.album.cover_small,
                    album_cover_medium: track.album.cover_medium
                };
            });
        }

        static isFirst(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === 0;
            }

            return false;
        }

        static isLast(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === array.length - 1;
            }

            return false;
        }

        static isEmpty(array) {
            return array.length === 0;
        }

        playerComponent() {
            return {

            }
        }

        searchComponent() {
            return {
                results: [],
                q: '',
                submitted: false,
                search() {
                    const self = this;

                    DZ.api(`search?q=${this.q}`, function (response) {
                        self.submitted = true;
                        self.results = Deezbox.transformTracks(response.data);
                    });
                },
                queue(track) {
                    Alpine.store('playlist').queue(track);
                },
                clear() {
                    this.submitted = false;
                    this.q = '';
                    this.results = [];
                },
                isFirst(track) {
                    return Deezbox.isFirst(this.results, track);
                },
                isLast(track) {
                    return Deezbox.isLast(this.results, track);
                },
                isEmpty() {
                    return Deezbox.isEmpty(this.results);
                }
            }
        }
    }

    document.addEventListener('alpine:init', function () {
        window.deezbox = new Deezbox();
    });
})();