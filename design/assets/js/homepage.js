angular.module('MotsDitsQuebec').controller('HomepageCtrl', function($scope, $http, $window, $cookies) {

  $scope.motsdits = [];

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

  // Load a list of motdits
  $http.get('/api/v1/motsdits?format=json').success(function(data) {
    $scope.motsdits = data;
  });

});
