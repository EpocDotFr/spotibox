(function () {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Api = class {
        spotifyId = null

        constructor(spotifyId) {
            this.spotifyId = spotifyId;
        }

        searchCatalog(q) {
            return this.fetch(
                'get',
                `room/${this.spotifyId}/catalog`,
                {
                    q: q
                }
            );
        }

        getPlaybackState() {
            return this.fetch(
                'get',
                `room/${this.spotifyId}/playback/state`
            );
        }

        startOrResumePlayback() {
            return this.fetch(
                'put',
                `room/${this.spotifyId}/playback`
            );
        }

        pausePlayback() {
            return this.fetch(
                'delete',
                `room/${this.spotifyId}/playback`
            );
        }

        previousTrack() {
            return this.fetch(
                'patch',
                `room/${this.spotifyId}/playback`
            );
        }

        nextTrack() {
            return this.fetch(
                'post',
                `room/${this.spotifyId}/playback`
            );
        }

        setVolume(volume) {
            return this.fetch(
                'put',
                `room/${this.spotifyId}/playback/volume`,
                null,
                {
                    volume: volume
                }
            );
        }

        seek(position) {
            return this.fetch(
                'put',
                `room/${this.spotifyId}/playback/position`,
                null,
                {
                    position: position
                }
            );
        }

        addToQueue(track_id) {
            return this.fetch(
                'post',
                `room/${this.spotifyId}/queue`,
                null,
                {
                    track_id: track_id
                }
            );
        }

        fetch(method, resource, params = null, json = null) {
            const url = new URL(`/api/${resource}`, window.location.origin);

            if (params) {
                Object.entries(params).forEach(function (param) {
                    const [name, value] = param;

                    url.searchParams.set(name, value);
                });
            }

            const headers = {
                'Accept': 'application/json',
            };

            let body = null;

            if (json) {
                headers['Content-Type'] = 'application/json';

                body = JSON.stringify(json);
            }

            return fetch(url, {
                method: method,
                headers: headers,
                body: body
            }).then(function (response) {
                const contentType = response.headers.get('Content-Type');

                if (contentType && contentType.includes('application/json')) {
                    return response.json()
                        .then(function (data) {
                            if (!response.ok) {
                                if ('message' in data) {
                                    if (typeof data.message === 'string') {
                                        throw new Error(data.message);
                                    } else {
                                        let message = '\n';

                                        Object.entries(data.message).forEach(function (param) {
                                            const [parameter, msg] = param;

                                            message += `\n${parameter}: ${msg}`;
                                        });

                                        throw new Error(message);
                                    }
                                } else {
                                    throw new Error('Unspecified error');
                                }
                            }

                            return data;
                        });
                } else {
                    throw new Error('JSON expected');
                }
            }).catch(function (error) {
                alert(`Error communicating with the backend: ${error.message}`);
            });
        }
    };
})();