(function() {
    'use strict';

    class DeezBox {
        constructor() {
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
    }

    document.addEventListener('alpine:init', function() {
        new DeezBox();
    });
}());