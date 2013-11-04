angular.module('MotsDitsQuebec').controller('HomepageCtrl', function($scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

});
