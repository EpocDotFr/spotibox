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
                    init() {
                        this.refresh();
                    },
                    refresh() {
                        const component = this;

                        room.api.getQueue()
                            .catch(function(error) {
                                alert(error);
                            })
                            .then(function(data) {
                                component.tracks = data;

                                setTimeout(function () {
                                    component.refresh();
                                }, 3000);
                            });
                    },
                    requeue($button, track) {
                        $button.disabled = true;

                        room.api.addToQueue(track.id)
                            .catch(function(error) {
                                $button.disabled = false;

                                alert(error);
                            })
                            .then(function(data) {
                                $button.disabled = false;
                            });
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
                    nowPlaying: null,
                    canPause: false,
                    canStartOrResume: false,
                    canSkipToNext: false,
                    canSkipToPrevious: false,
                    init() {
                        this.refresh();
                    },
                    refresh() {
                        const component = this;

                        room.api.getPlaybackStatus()
                            .catch(function(error) {
                                alert(error);
                            })
                            .then(function(data) {
                                component.nowPlaying = data.now_playing;
                                component.canPause = data.can_pause;
                                component.canStartOrResume = data.can_start_or_resume;
                                component.canSkipToNext = data.can_skip_to_next;
                                component.canSkipToPrevious = data.can_skip_to_previous;

                                setTimeout(function () {
                                    component.refresh();
                                }, 3000);
                            });
                    },
                    prev($button) {
                        $button.disabled = true;

                        room.api.previousTrack()
                            .catch(function(error) {
                                $button.disabled = false;

                                alert(error);
                            })
                            .then(function(data) {
                                $button.disabled = false;
                            });
                    },
                    playPause($button) {
                        $button.disabled = true;

                        if (this.canPause) {
                            room.api.pausePlayback()
                                .catch(function(error) {
                                    $button.disabled = false;

                                    alert(error);
                                })
                                .then(function(data) {
                                    $button.disabled = false;
                                });
                        } else if (this.canStartOrResume) {
                            room.api.startOrResumePlayback()
                                .catch(function(error) {
                                    $button.disabled = false;

                                    alert(error);
                                })
                                .then(function(data) {
                                    $button.disabled = false;
                                });
                        }
                    },
                    next($button) {
                        $button.disabled = true;

                        room.api.nextTrack()
                            .catch(function(error) {
                                $button.disabled = false;

                                alert(error);
                            })
                            .then(function(data) {
                                $button.disabled = false;
                            });
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

                                alert(error);
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

                                alert(error);
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