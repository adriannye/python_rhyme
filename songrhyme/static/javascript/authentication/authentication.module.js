(function () {
  'use strict';

  angular
    .module('songrhyme.authentication', [
      'songrhyme.authentication.controllers',
      'songrhyme.authentication.services'
    ]);

  angular
    .module('songrhyme.authentication.controllers', []);

  angular
    .module('songrhyme.authentication.services', ['ngCookies']);
})();
