/**
* AddWordController
* @namespace songrhyme.rhyme.controllers
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.controllers')
    .controller('AddWordController', AddWordController);

  AddWordController.$inject = ['$location', '$scope', 'Rhyme'];

  /**
  * @namespace AddWordController
  */
  function AddWordController($location, $scope, Rhyme) {
    var vm = this;

    vm.add_word = add_word;
    vm.typed = Rhyme.typed;

    /**
    * @name add_word
    * @desc Add a word to rhyme list
    * @memberOf songrhyme.rhyme.controllers.AddWordController
    */
    function add_word() {
        Rhyme.add_word_to_rhymes(vm.add_word_rhyme);
    }

  }
})();
