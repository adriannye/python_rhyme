(function () {
  'use strict';

  angular
    .module('songrhyme', [
      'songrhyme.routes',
      'songrhyme.config',
      'songrhyme.layout',
      'songrhyme.authentication',
      'songrhyme.rhyme'
    ]);

  angular
    .module('songrhyme.routes', ['ngRoute']);
  angular
    .module('songrhyme.config', []);
})();

angular
  .module('songrhyme')
  .run(run);

run.$inject = ['$http'];

/**
* @name run
* @desc Update xsrf $http headers to align with Django's defaults
*/
function run($http) {
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.xsrfCookieName = 'csrftoken';
}
