(function() {
    'use strict';

    class Deezbox {
        pusherKey = '54c230647abc0f6ac73d';
        pusherCluster = 'eu';

        deezerAppId = '632324';

        constructor() {
            this.getDomNodes();

            /*this.pusher = new Pusher(this.pusherKey, {
              cluster: this.pusherCluster
            });

            this.pusherChannel = this.pusher.subscribe('deezbox');

            this.deezer = DZ.init({
                appId: this.deezerAppId,
                //channelUrl: 'http://developers.deezer.com/examples/channel.php'
            });*/

            /*Alpine.store('radios', [
                {
                    title: 'PulsRadio 00s',
                    websiteUrl: 'https://www.pulsradio.com',
                    source: 'http://icecast.pulsradio.com/puls00HD.mp3',
                }
            ]);
            Alpine.store('nowPlaying', {
                init() {
                    this.radio = {name: 'PulsRadio 00s', url: 'https://www.pulsradio.com'};
                },

                radio: null,
            });*/
        }

        getDomNodes() {

        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const db = new Deezbox();
    });
}());
