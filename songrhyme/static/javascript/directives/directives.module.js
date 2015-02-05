(function () {
  'use strict';

  var app = angular
    .module('songrhyme.directives', []);


  app.directive('focusOnPageLoad',function($timeout){
    return {
        link: function(scope, element, attrs) {
            element[0].focus();
        }
    };
  });
})();
