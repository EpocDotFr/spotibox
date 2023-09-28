(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Room = class {
        api = null

        constructor(spotifyId) {
            this.api = new Spotibox.Api(spotifyId);

            //this.initDeezer();
            this.initAlpine();
            // this.initPusher();
        }

        /*initDeezer() {
            DZ.init({
                appId: this.deezerAppId,
                channelUrl: `${window.location.origin}/channel.html`,
                player: {
                    onload: function (player) {
                        DZ.Event.subscribe('player_play', function () {
                            Alpine.store('playerComponent').isPlaying = true;
                        });

                        DZ.Event.subscribe('player_paused', function () {
                            Alpine.store('playerComponent').isPlaying = false;
                        });

                        DZ.Event.subscribe('current_track', function (track) {
                            Alpine.store('playerComponent').nowPlaying = Alpine.store('playlistComponent').track(track.index);
                        });
                    }
                }
            });
        }*/

        initAlpine() {
            const room = this;

            Alpine.store('playlistComponent', {
                tracks: [],
                track(index) {
                    return this.tracks[index];
                },
                queue(track) {
                    this.tracks.push(Object.assign({}, track));
                },
                clear() {
                    this.tracks = [];
                },
                isFirst(track) {
                    return Spotibox.Utils.isFirst(this.tracks, track);
                },
                isLast(track) {
                    return Spotibox.Utils.isLast(this.tracks, track);
                },
                isEmpty() {
                    return Spotibox.Utils.isEmpty(this.tracks);
                }
            });

            Alpine.store('playerComponent', {
                nowPlaying: {},
                isPlaying: false,
                get canUseControls() {
                    return !Alpine.store('playlistComponent').isEmpty();
                },
                prev() {
                    //DZ.player.prev();
                },
                playPause() {
                    /*if (this.isPlaying) {
                        DZ.player.pause();
                    } else {
                        DZ.player.play();
                    }*/
                },
                next() {
                    //DZ.player.next();
                }
            });

            Alpine.data('searchComponent', function() {
                return {
                    results: [],
                    q: '',
                    submitted: false,
                    search() {
                        const component = this;

                        room.api.search(this.q).then(function(data) {
                            component.results = data; // FIXME Do not work
                        })
                    },
                    queue(track) {
                        Alpine.store('playlistComponent').queue(track);
                    },
                    clear() {
                        this.results = [];
                        this.q = '';
                        this.submitted = false;
                    },
                    isFirst(track) {
                        return Spotibox.Utils.isFirst(this.results, track);
                    },
                    isLast(track) {
                        return Spotibox.Utils.isLast(this.results, track);
                    },
                    isEmpty() {
                        return Spotibox.Utils.isEmpty(this.results);
                    }
                };
            });
        }

        /*initPusher() {
            this.pusher = new Pusher(this.pusherKey, {
                cluster: this.pusherCluster
            });

            this.pusherChannel = this.pusher.subscribe('room');
        }*/
    };
})();