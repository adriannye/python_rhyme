/**
* LogoutController
* @namespace songrhyme.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('songrhyme.authentication.controllers')
    .controller('LogoutController', LogoutController);

  LogutController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace LogutController
  */
  function LoginController($location, $scope, Authentication) {
    var vm = this;

    vm.logout = logout;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf songrhyme.authentication.controllers.LogutController
    */
    function activate() {
      // If the user is unauthenticated, they should not be here.
      if (!Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name logout
    * @desc Log the user in
    * @memberOf songrhyme.authentication.controllers.LogutController
    */
    function logout() {
      Authentication.logout(vm.email);
    }
  }
})();
