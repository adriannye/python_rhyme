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
    $routeProvider.when('/rhyme/word', {
      controller: 'WordController', 
      controllerAs: 'vm',
      templateUrl: '/static/templates/rhyme/word.html'
    }).when('/rhyme/rhymes', {
      controller: 'RhymeController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/rhyme/rhymes.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).otherwise('/rhyme');
  }
})();