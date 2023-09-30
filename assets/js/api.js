(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Api = class {
        spotifyId = null

        constructor(spotifyId) {
            this.spotifyId = spotifyId;
        }

        search(q) {
            return this.fetch(
                'get',
                `room/${this.spotifyId}/catalog`,
                {
                    q: q
                }
            );
        }

        queue(track_id) {
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

            return fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: json ? JSON.stringify(json) : null
            }).then(function(response) {
                if (response.ok) {
                    return response.json();
                }

                return Promise.reject(response);
            }).catch(function(error) {
                alert(error);
            });
        }
    };
})();