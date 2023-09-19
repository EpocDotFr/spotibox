(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Room = class {
        constructor() {
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
            Alpine.store('playlistComponent', {
                tracks: [],
                track(index) {
                    return this.tracks[index];
                },
                queue(track) {
                    this.tracks.push(Object.assign({}, track));
                },
                remove(track) {
                    const index = this.tracks.indexOf(track);

                    if (index > -1) {
                        this.tracks.splice(index, 1);
                    }
                },
                clear() {
                    this.tracks = [];
                },
                moveUp(track) {
                    Spotibox.Room.move(this.tracks, track, 'up');
                },
                moveDown(track) {
                    Spotibox.Room.move(this.tracks, track, 'down');
                },
                /*syncWithDeezerPlayer() {
                    DZ.player.playTracks(
                        this.tracks.map(function (track) {
                            return track.id;
                        }),
                        false
                    );
                },*/
                isFirst(track) {
                    return Spotibox.Room.isFirst(this.tracks, track);
                },
                isLast(track) {
                    return Spotibox.Room.isLast(this.tracks, track);
                },
                isEmpty() {
                    return Spotibox.Room.isEmpty(this.tracks);
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

            Alpine.store('searchComponent', {
                results: [],
                q: '',
                submitted: false,
                search() {
                    const self = this;

                    /*DZ.api(`search?q=${this.q}`, function (response) {
                        self.submitted = true;
                        self.results = Spotibox.Room.transformTracks(response.data);
                    });*/
                },
                queue(track) {
                    Alpine.store('playlistComponent').queue(track);
                },
                clear() {
                    this.submitted = false;
                    this.q = '';
                    this.results = [];
                },
                isFirst(track) {
                    return Spotibox.Room.isFirst(this.results, track);
                },
                isLast(track) {
                    return Spotibox.Room.isLast(this.results, track);
                },
                isEmpty() {
                    return Spotibox.Room.isEmpty(this.results);
                }
            });
        }

        /*initPusher() {
            this.pusher = new Pusher(this.pusherKey, {
                cluster: this.pusherCluster
            });

            this.pusherChannel = this.pusher.subscribe('room');
        }*/

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

        static move(array, item, direction) {
            const index = array.indexOf(item);
            const newIndex = direction === 'up' ? index - 1 : index + 1;

            if (index > -1 && newIndex >= 0 && newIndex <= array.length) {
                array.splice(index, 1);
                array.splice(newIndex , 0, item);
            }
        }
    }
})();