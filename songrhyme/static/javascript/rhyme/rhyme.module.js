(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme', [
      'songrhyme.rhyme.controllers',
      'songrhyme.rhyme.directives',
      'songrhyme.rhyme.services'
    ]);

  angular
    .module('songrhyme.rhyme.controllers', []);

  angular
    .module('songrhyme.rhyme.directives', []);

  angular
    .module('songrhyme.rhyme.services', ['ngCookies']);
})();
