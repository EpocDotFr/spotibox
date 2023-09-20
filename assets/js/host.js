(function() {
    'use strict';

    window.Spotibox.Host = class {
        spotifyRedirectUri = null;
        spotifyClientId = null;

        constructor(spotifyRedirectUri, spotifyClientId) {
            this.spotifyRedirectUri = spotifyRedirectUri;
            this.spotifyClientId = spotifyClientId;

            const host = this;

            Alpine.store('hostComponent', {
                spotify: {
                    connected: false,
                    token: null,
                    accountName: null,
                    codeVerifier: null
                }, // Alpine.$persist(
                error: null,
                init() {
                    const searchParams = new URLSearchParams(document.location.search);
                    const code = searchParams.get('code');
                    const error = searchParams.get('error');

                    if (code) {
                        // this.spotify.connected = true;
                        // this.spotify.token = '';
                        // this.spotify.accountName = '';
                        // this.spotify.codeVerifier = null;
                    } else if (error) {
                        switch (error) {
                            case 'access_denied':
                                this.error = 'You did not authorize Spotibox to access your Spotify account.';
                            break;
                            default:
                                this.error = `Got error code "${error}" from Spotify.`;
                        }

                        this.spotify.connected = false;
                        this.spotify.token = null;
                        this.spotify.accountName = null;
                        this.spotify.codeVerifier = null;
                    }
                },
                connect() {
                    const codeVerifier = Spotibox.generateRandomString(128);

                    const component = this;

                    Spotibox.Host.generateCodeChallenge(codeVerifier).then(function (codeChallenge) {
                        let state = Spotibox.generateRandomString(16);
                        let scope = 'user-read-private streaming user-modify-playback-state';

                        component.spotify.codeVerifier = codeVerifier;

                        const url = new URL('https://accounts.spotify.com/authorize');

                        url.searchParams.set('response_type', 'code');
                        url.searchParams.set('client_id', host.spotifyClientId);
                        url.searchParams.set('scope', scope);
                        url.searchParams.set('redirect_uri', host.spotifyRedirectUri); // 'http://localhost:8080/host'
                        url.searchParams.set('state', state);
                        url.searchParams.set('code_challenge_method', 'S256');
                        url.searchParams.set('code_challenge', codeChallenge);

                        window.location.href = url.toString();
                    });
                },
                disconnect() {
                    this.spotify.connected = false;
                    this.spotify.token = null;
                    this.spotify.accountName = null;
                    this.spotify.codeVerifier = null;
                }
            });
        }

        static async generateCodeChallenge(codeVerifier) {
            const encoder = new TextEncoder();
            const data = encoder.encode(codeVerifier);
            const digest = await window.crypto.subtle.digest('SHA-256', data);

            return Spotibox.base64encode(digest);
        }
    };
})();