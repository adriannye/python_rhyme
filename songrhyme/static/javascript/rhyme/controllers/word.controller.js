/**
* WordController
* @namespace songrhyme.rhyme.controllers
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.controllers')
    .controller('WordController', WordController);

  WordController.$inject = ['$location', '$scope', 'Rhyme'];

  /**
  * @namespace WordController
  */
  function WordController($location, $scope, Rhyme) {
    var vm = this;

    vm.submit_word = submit_word;

    /**
    * @name word
    * @desc Get a word to rhyme 
    * @memberOf songrhyme.rhyme.controllers.WordController
    */
    function submit_word() {
        Rhyme.rhymes_for_word(vm.word_to_rhyme);
    }

  }
})();
