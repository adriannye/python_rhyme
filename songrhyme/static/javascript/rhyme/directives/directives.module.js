(function () {
  'use strict';

  angular
    .module('songrhyme.rhyme.directives', [])
    .directive('focusOnPageLoad',function($timeout){
        return {
            scope: {
                focusInfo: '='
            },
            link: function(scope, element, attrs) {
                element[0].focus();
            }
        };
    })
    .directive('fbLike', [ '$window', '$rootScope', function ($window, $rootScope) {
          return {
              restrict: 'A',
              scope: {
                  fbLike: '=?'
              },
              link: function (scope, element, attrs) {
                  if (!$window.FB) {
                      // Load Facebook SDK if not already loaded
                      $.getScript('//connect.facebook.net/en_US/sdk.js', function () {
                          $window.FB.init({
                              appId: '572549126214344',
                              xfbml: true,
                              version: 'v2.0'
                          });
                          renderLikeButton();
                      });
                  } else {
                      renderLikeButton();
                  }
 
                  var watchAdded = false;
                  function renderLikeButton() {
                      if (!!attrs.fbLike && !scope.fbLike && !watchAdded) {
                          // wait for data if it hasn't loaded yet
                          var watchAdded = true;
                          var unbindWatch = scope.$watch('fbLike', function (newValue, oldValue) {
                              if (newValue) {
                                  renderLikeButton();
                                   
                                  // only need to run once
                                  unbindWatch();
                              }
                               
                          });
                          return;
                      } else {
                          element.html('<div class="fb-like"' + (!!scope.fbLike ? ' data-href="' + scope.fbLike + '"' : '') + ' data-layout="button_count" data-action="like" data-show-faces="true" data-share="true"></div>');
                          $window.FB.XFBML.parse(element.parent()[0]);
                      }
                  }
              }
          };
      }
  ]);

})();
