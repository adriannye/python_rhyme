(function () {
  'use strict';

  angular
    .module('songrhyme.config')
    .config(config);

  config.$inject = ['$locationProvider', '$logProvider'];

  /**
  * @name config
  * @desc Enable HTML5 routing
  */
  function config($locationProvider, $logProvider) {
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
    $logProvider.debugEnabled(true);
  }
})();
