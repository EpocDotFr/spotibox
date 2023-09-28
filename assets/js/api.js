(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Api = class {
        spotifyId = null

        constructor(spotifyId) {
            this.spotifyId = spotifyId;
        }

        search(q) {
            return this.call(
                'get',
                `room/${this.spotifyId}/catalog`,
                {
                    q: q
                }
            );
        }

        call(method, resource, params = null, json = null) {
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
                } else {
                    return Promise.reject(response);
                }
            }).catch(function(error) {
                alert(error);
            });
        }
    };
})();