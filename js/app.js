(function() {
    'use strict';

    window.Deezbox = class {
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
                    this.tracks.push(track);
                },
                remove: function (track) {
                    const i = this.tracks.indexOf(track);

                    if (i > -1) {
                        this.tracks.splice(i, 1);
                    }
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

        // ---------------------------------------------------------------------------
        // Player

        static playerComponent() {
            return {

            }
        }

        // ---------------------------------------------------------------------------
        // Playlist

        static playlistComponent() {
            return {
                requeue(track) {
                    Alpine.store('playlist').queue(track);
                },
                remove(track) {
                    Alpine.store('playlist').remove(track);
                },
                clear() {
                    console.log('clear');
                }
            }
        }

        // ---------------------------------------------------------------------------
        // Search

        static searchComponent() {
            return {
                results: [],
                q: '',
                submitted: false,
                search() {
                    const self = this;

                    DZ.api(`search?q=${this.q}`, function(response) {
                        self.submitted = true;
                        self.results = window.Deezbox.transformTracks(response.data);
                    });
                },
                queue(track) {
                    Alpine.store('playlist').queue(track);
                },
                clear() {
                    this.submitted = false;
                    this.q = '';
                    this.results = [];
                }
            }
        }
    }

    document.addEventListener('alpine:init', function() {
        window.db = new window.Deezbox();
    });
})();