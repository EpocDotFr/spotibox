(function() {
    'use strict';

    class Deezbox {
        pusherKey = '54c230647abc0f6ac73d';
        pusherCluster = 'eu';

        deezerAppId = '632324';

        constructor() {
            /*this.pusher = new Pusher(this.pusherKey, {
              cluster: this.pusherCluster
            });

            this.pusherChannel = this.pusher.subscribe('room');*/

            DZ.init({
                appId: this.deezerAppId,
                channelUrl: `${window.location.origin}/channel.html`
            });
        }

        // ---------------------------------------------------------------------------
        // Playlist

        playlistFragment() {
            return {
                playlist: [],
                requeue() {
                    console.log('requeue');
                },
                remove() {
                    console.log('remove');
                }
            }
        }

        // ---------------------------------------------------------------------------
        // Search

        searchFragment() {
            return {
                results: [],
                q: '',
                search() {
                    const self = this;

                    DZ.api(`search?q=${this.q}`, function(response) {
                        self.results = response.data;
                    });
                },
                queue() {
                    console.log('queue');
                }
            }
        }
    }

    document.addEventListener('alpine:init', function() {
        window.deezbox = new Deezbox();
    });
})();