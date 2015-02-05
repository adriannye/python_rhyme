(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.directives', [])
    .directive('focusOnPageLoad',function($timeout){
    return {
        scope: {
            focusInfo: '=info'
        },
        link: function(scope, element, attrs) {
            console.log('focusing');
            element[0].focus();
        }
    };
  });
})();
