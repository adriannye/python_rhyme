/**
* WordController
* @namespace songrhyme.rhyme.controllers
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.controllers')
    .controller('WordController', WordController);

  WordController.$inject = ['$location', '$scope'];

  /**
  * @namespace WordController
  */
  function WordController($location, $scope) {
    var vm = this;

    vm.word = word;

    /**
    * @name word
    * @desc Get a word to rhyme 
    * @memberOf songrhyme.rhyme.controllers.WordController
    */
    function word() {
      alert(vm.word_to_rhyme);
      $location.url('/rhymes/' + vm.word_to_rhyme + '/');
    }
  }
})();
