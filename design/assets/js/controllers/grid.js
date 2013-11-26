angular.module('MotsDitsQuebec').controller('GridCtrl', function($scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

});
