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

            DZ.api('/playlist/10919883502', function(response) {
                Alpine.store('playlist', response.tracks.data);
            });
        }
    }

    document.addEventListener('alpine:init', function() {
        Alpine.store('playlist', []);
    });

    document.addEventListener('DOMContentLoaded', function() {
        window.deezbox = new Deezbox();
    });
})();