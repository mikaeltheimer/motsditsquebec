/**
 * Header controller
 * Handles all logic related to the header bar
 */
angular.module('MotsDitsQuebec').controller('HeaderCtrl', function($rootScope, $scope, $http, $location, $window, $cookies, $log) {

  /**
   * Perform a global search
   */
  $scope.doGlobalSearch = function(ev, query){
    if(ev.which == 13) $window.location.href = "/?search=" + query;
  };

});
