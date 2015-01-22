/**
* Rhyme
* @namespace songrhyme.rhyme.services
*/
(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.services')
    .factory('Rhyme', Rhyme);

  Rhyme.$inject = ['$cookies', '$http', '$location'];

  /**
  * @namespace Rhyme
  * @returns {Factory}
  */
  function Rhyme($cookies, $http, $location) {
    /**
    * @name Rhyme
    * @desc The Factory to be returned
    */

    var rhyme_data;
    var typed;

    var Rhyme = {
      rhymes_for_word: rhymes_for_word,
      rhyme_data: rhyme_data,
      typed: typed
    };

    return Rhyme;

    /**
    * @name rhymes_for_word
    * @desc get rhyme data for the word entered by user
    * @param {string} word The word entered by the user
    * @returns {Promise}
    * @memberOf songrhyme.rhyme.services.Rhyme
    */
    function rhymes_for_word(word) {
      Rhyme.typed = word;
      console.log(word);
      return $http.get('/rhyme/api/rhymes_for_word/' + word + '/', {
        }).then(wordSuccessFn, wordErrorFn);

      /**
      * @name wordSuccessFn
      * @desc Get rhymes
      */
      function wordSuccessFn(data, status, headers, config) {
          Rhyme.rhyme_data = data.data;
          $location.url('/rhyme/rhymes/');
      }

      /**
      * @name wordErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function wordErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }
  }
})();
