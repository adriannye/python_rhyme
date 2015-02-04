/**
* RhymeController
* @namespace songrhyme.rhyme.controllers
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.controllers')
    .controller('RhymeController', RhymeController);

  RhymeController.$inject = ['$location', '$scope', 'Rhyme'];

  /**
  * @namespace RhymeController
  */
  function RhymeController($location, $scope, Rhyme) {
    var vm = this;

    vm.rhyme_data = Rhyme.rhyme_data;
    vm.typed = Rhyme.typed;
    $scope.search = {
        'pos': '!9'
    };
    
  }
})();
