(function () {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Room = class {
        api = null

        constructor(spotifyId) {
            this.api = new Spotibox.Api(spotifyId);

            this.initAlpine();
            this.refresh();
        }

        initAlpine() {
            const room = this;

            Alpine.store('playerComponent', {
                canPause: false,
                canStartOrResume: false,
                canSeek: false,
                canSkipToNext: false,
                canSkipToPrevious: false,
                volume: 0,
                oldVolume: null,
                canChangeVolume: false,
                nowPlaying: null,
                showRemaining: false,
                remainingText: '',
                progressText: '',
                progressMs: 0,
                prev($button) {
                    $button.disabled = true;

                    room.api.previousTrack()
                        .catch(function (error) {
                            $button.disabled = false;
                        })
                        .then(function (data) {
                            $button.disabled = false;
                        });
                },
                playPause($button) {
                    $button.disabled = true;

                    if (this.canPause) {
                        room.api.pausePlayback()
                            .catch(function (error) {
                                $button.disabled = false;
                            })
                            .then(function (data) {
                                $button.disabled = false;
                            });
                    } else if (this.canStartOrResume) {
                        room.api.startOrResumePlayback()
                            .catch(function (error) {
                                $button.disabled = false;
                            })
                            .then(function (data) {
                                $button.disabled = false;
                            });
                    }
                },
                next($button) {
                    $button.disabled = true;

                    room.api.nextTrack()
                        .catch(function (error) {
                            $button.disabled = false;
                        })
                        .then(function (data) {
                            $button.disabled = false;
                        });
                },
                muteUnmute($button) {
                    $button.disabled = true;

                    let newVolume = null;

                    if (this.volume > 0) {
                        newVolume = 0;

                        this.oldVolume = this.volume;
                    } else if (this.oldVolume) {
                        newVolume = this.oldVolume;

                        this.oldVolume = null;
                    }

                    room.api.setVolume(newVolume)
                        .catch(function (error) {
                            $button.disabled = false;
                        })
                        .then(function (data) {
                            $button.disabled = false;
                        });
                },
                setVolume($input) {
                    $input.disabled = true;

                    room.api.setVolume(this.volume)
                        .catch(function (error) {
                            $input.disabled = false;
                        })
                        .then(function (data) {
                            $input.disabled = false;
                        });
                },
                seek($input) {
                    $input.disabled = true;

                    room.api.seek(this.progressMs)
                        .catch(function (error) {
                            $input.disabled = false;
                        })
                        .then(function (data) {
                            $input.disabled = false;
                        });
                }
            });

            Alpine.store('queueComponent', {
                totalText: '',
                queue: [],
                requeue($button, track) {
                    $button.disabled = true;

                    room.api.addToQueue(track.id)
                        .catch(function (error) {
                            $button.disabled = false;
                        })
                        .then(function (data) {
                            $button.disabled = false;
                        });
                },
                isFirst(track) {
                    return Spotibox.Utils.isFirst(this.queue, track);
                },
                isLast(track) {
                    return Spotibox.Utils.isLast(this.queue, track);
                },
                isEmpty() {
                    return Spotibox.Utils.isEmpty(this.queue);
                }
            });

            Alpine.data('searchComponent', function () {
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
                            .catch(function (error) {
                                component.submitting = false;
                            })
                            .then(function (data) {
                                component.results = data;
                                component.submitted = true;
                                component.submitting = false;
                            });
                    },
                    queue($button, track) {
                        $button.disabled = true;

                        room.api.addToQueue(track.id)
                            .catch(function (error) {
                                $button.disabled = false;
                            })
                            .then(function (data) {
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

        refresh() {
            const room = this;
            const playerComponent = Alpine.store('playerComponent');
            const queueComponent = Alpine.store('queueComponent');

            this.api.getPlaybackState()
                .then(function (data) {
                    playerComponent.canPause = data.can_pause;
                    playerComponent.canStartOrResume = data.can_start_or_resume;
                    playerComponent.canSeek = data.can_seek;
                    playerComponent.canSkipToNext = data.can_skip_to_next;
                    playerComponent.canSkipToPrevious = data.can_skip_to_previous;
                    playerComponent.volume = data.volume;
                    playerComponent.canChangeVolume = data.can_change_volume;
                    playerComponent.nowPlaying = data.now_playing;
                    playerComponent.progressText = data.progress_text;
                    playerComponent.remainingText = data.remaining_text;
                    playerComponent.progressMs = data.progress_ms;
                    queueComponent.totalText = data.total_text;
                    queueComponent.queue = data.queue;

                    setTimeout(function () {
                        room.refresh();
                    }, 3000);
                });
        }
    };
})();