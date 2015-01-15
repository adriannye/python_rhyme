(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme', [
      'songrhyme.rhyme.controllers',
      'songrhyme.rhyme.services'
    ]);

  angular
    .module('songrhyme.rhyme.controllers', []);

  angular
    .module('songrhyme.rhyme.services', ['ngCookies']);
})();
