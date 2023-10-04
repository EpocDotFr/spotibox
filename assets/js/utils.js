(function () {
    'use strict';

    window.Spotibox = window.Spotibox || {};

    window.Spotibox.Utils = {
        isFirst(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === 0;
            }

            return false;
        },

        isLast(array, item) {
            const index = array.indexOf(item);

            if (index > -1) {
                return index === array.length - 1;
            }

            return false;
        },

        isEmpty(array) {
            return array.length === 0;
        }
    };
})();