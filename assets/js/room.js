(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Room = class {
        api = null

        constructor(spotifyId) {
            this.api = new Spotibox.Api(spotifyId);

            this.initAlpine();
        }

        initAlpine() {
            const room = this;

            Alpine.data('playlistComponent', function() {
                return {
                    tracks: [],
                    requeue($button, track) {
                        // TODO
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
                };
            });

            Alpine.data('playerComponent', function() {
                return {
                    nowPlaying: {},
                    isPlaying: false,
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
                }
            });

            Alpine.data('searchComponent', function() {
                return {
                    results: [],
                    q: '',
                    submitting: false,
                    submitted: false,
                    search() {
                        if (this.submitting) {
                            return;
                        }

                        this.submitting = true;

                        const component = this;

                        room.api.searchCatalog(this.q)
                            .catch(function(error) {
                                component.submitting = false;
                            })
                            .then(function(data) {
                                component.results = data;
                                component.submitted = true;
                                component.submitting = false;
                            });
                    },
                    queue($button, track) {
                        $button.disabled = true;

                        room.api.addToQueue(track.id)
                            .catch(function(error) {
                                $button.disabled = false;
                            })
                            .then(function(data) {
                                $button.disabled = false;
                            });
                    },
                    clear() {
                        this.results = [];
                        this.q = '';
                        this.submitting = false;
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
    };
})();