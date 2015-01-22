/**
* Register controller
* @namespace songrhyme.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication) {
    var vm = this;

    vm.register = register;
    vm.activate = activate;

    /**
    * @name register
    * @desc Register a new user
    * @memberOf songrhyme.authentication.controllers.RegisterController
    */
    function register() {
      Authentication.register(vm.email, vm.password, vm.first_name, vm.last_name);
    }

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf songrhyme.authentication.controllers.RegisterController
     */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }
  }
})();
