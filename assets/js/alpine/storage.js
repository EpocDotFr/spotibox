(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};
    window.Spotibox.Alpine = window.Spotibox.Alpine || {};

    window.Spotibox.Alpine.Storage = function () {
        Alpine.store('storage', {
            spotify: Alpine.$persist({ // FIXME Marche pas
                connected: false,
                accessToken: null,
                refreshToken: null,
                accountName: null,
                codeVerifier: null
            })
        });
    };
})();