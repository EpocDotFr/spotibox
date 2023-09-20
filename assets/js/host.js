(function() {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Host = class {
        spotifyRedirectUri = null;
        spotifyClientId = null;

        constructor(spotifyRedirectUri, spotifyClientId) {
            this.spotifyRedirectUri = spotifyRedirectUri;
            this.spotifyClientId = spotifyClientId;

            this.initAlpine();
        }

        initAlpine() {
            const host = this;

            Spotibox.Alpine.Storage();

            Alpine.data('hostComponent', function () {
                return {
                    error: null,
                    init() {
                        const searchParams = new URLSearchParams(document.location.search);
                        const code = searchParams.get('code');
                        const error = searchParams.get('error');
                        const component = this;

                        if (code) {
                            const body = new URLSearchParams({
                                grant_type: 'authorization_code',
                                code: code,
                                redirect_uri: host.spotifyRedirectUri,
                                client_id: host.spotifyClientId,
                                code_verifier: Alpine.store('storage').spotify.codeVerifier
                            });

                            fetch('https://accounts.spotify.com/api/token', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                },
                                body: body
                            }).then(function(response) {
                                if (response.ok) {
                                    return response.json();
                                } else {
                                    component.error = `Failed to get access token from Spotify (got error ${response.status}).`;
                                }
                            }).then(function(data) {
                                Alpine.store('storage').spotify.connected = true;
                                Alpine.store('storage').spotify.accessToken = data.access_token;
                                Alpine.store('storage').spotify.refreshToken = data.refresh_token;
                                Alpine.store('storage').spotify.codeVerifier = null;

                                const spotifyWebApi = new SpotifyWebApi();

                                spotifyWebApi.setAccessToken(data.access_token);

                                spotifyWebApi.getMe().then(
                                    function (data) {
                                        Alpine.store('storage').spotify.accountName = data.display_name;
                                    },
                                    function (error) {
                                        component.error = `Error getting user profile data from Spotify: ${error}.`;
                                    }
                                );

                            }).catch(function(error) {
                                component.error = `Error getting access token from Spotify: ${error}.`;
                            });
                        } else if (error) {
                            Alpine.store('storage').spotify.codeVerifier = null;

                            switch (error) {
                                case 'access_denied':
                                    this.error = 'You did not authorize Spotibox to access your Spotify account.';
                                break;
                                default:
                                    component.error = `Got error code "${error}" from Spotify.`;
                            }
                        }
                    },
                    connect() {
                        const codeVerifier = Spotibox.Utils.generateRandomString(128);
                        const component = this;

                        Spotibox.Host.generateCodeChallenge(codeVerifier).then(function (codeChallenge) {
                            let state = Spotibox.Utils.generateRandomString(16);
                            let scope = 'user-read-private streaming user-modify-playback-state';

                            Alpine.store('storage').spotify.codeVerifier = codeVerifier;

                            const url = new URL('https://accounts.spotify.com/authorize');

                            url.searchParams.set('response_type', 'code');
                            url.searchParams.set('client_id', host.spotifyClientId);
                            url.searchParams.set('scope', scope);
                            url.searchParams.set('redirect_uri', host.spotifyRedirectUri);
                            url.searchParams.set('state', state);
                            url.searchParams.set('code_challenge_method', 'S256');
                            url.searchParams.set('code_challenge', codeChallenge);

                            window.location.href = url.toString();
                        });
                    },
                    disconnect() {
                        Alpine.store('storage').spotify.connected = false;
                        Alpine.store('storage').spotify.accessToken = null;
                        Alpine.store('storage').spotify.refreshToken = null;
                        Alpine.store('storage').spotify.accountName = null;
                        Alpine.store('storage').spotify.codeVerifier = null;
                    }
                };
            });
        }

        static async generateCodeChallenge(codeVerifier) {
            const encoder = new TextEncoder();
            const data = encoder.encode(codeVerifier);
            const digest = await window.crypto.subtle.digest('SHA-256', data);

            return Spotibox.Utils.base64encode(digest);
        }
    };
})();