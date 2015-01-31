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

    var typed;  // user entered word to rhyme
    var add_word_rhyme;  // user entered word that rhymes with "typed"
    var rhyme_data;  // data returned from rhyme web service

    var Rhyme = {
      // functions
      rhymes_for_word: rhymes_for_word,
      add_word_to_rhymes: add_word_to_rhymes,

      // data
      typed: typed,
      add_word_rhyme: add_word_rhyme,
      rhyme_data: rhyme_data
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
      return $http.get('/rhyme/api/rhymes_for_word/' + word + '/', {
        }).then(wordSuccessFn, wordErrorFn);

      /**
      * @name wordSuccessFn
      * @desc Redirect to show rhymes or add word
      */
      function wordSuccessFn(data, status, headers, config) {
          Rhyme.rhyme_data = data.data;
          if (data.data.error) {
             $location.url('/rhyme/addword/');
          } else {
             $location.url('/rhyme/rhymes/');
          }
      }

      /**
      * @name wordErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function wordErrorFn(data, status, headers, config) {
        console.error('failure getting rhymes!');
      }
    }

    /**
    * @name add_word_to_rhymes
    * @desc add a word to the database 
    * @param {string} word The word that has no rhyme yet
    * @param {string} rhyme The word that it rhymes with that we hopefully already know
    * @returns {Promise}
    * @memberOf songrhyme.rhyme.services.Rhyme
    */
    function add_word_to_rhymes(add_word_rhyme) {
      Rhyme.add_word_rhyme = add_word_rhyme;
      return $http.post('/rhyme/api/add_word/' + Rhyme.typed + '/' + add_word_rhyme + '/', {
        }).then(wordSuccessFn, wordErrorFn);

      /**
      * @name wordSuccessFn
      * @desc Get rhymes
      */
      function wordSuccessFn(data, status, headers, config) {
          Rhyme.rhyme_data = data.data;
          if (data.data.error) {
             $location.url('/rhyme/addword/');
          } else {
              Rhyme.rhymes_for_word(Rhyme.typed);
          }
      }

      /**
      * @name wordErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function wordErrorFn(data, status, headers, config) {
        console.error('failure adding word to rhyme list!');
      }
    }
  }
})();
