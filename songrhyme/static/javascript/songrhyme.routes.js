(function () {
  'use strict';

  angular
    .module('songrhyme.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/word', {
      controller: 'WordController', 
      controllerAs: 'vm',
      templateUrl: '/static/templates/rhyme/word.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/rhymes', {
      controller: 'RhymesController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/rhyme/rhymes.html'
    }).otherwise('/');
  }
})();
