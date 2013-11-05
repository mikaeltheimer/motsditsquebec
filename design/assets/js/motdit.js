
angular.module('MotsDitsQuebec').controller('MotDitCtrl', function($scope, $http, $window, $cookies) {

  // Motdit data
  $scope.motdit = {};
  // Related objects
  $scope.related = [];

  var motdit_id = (/mot\/([^\/]+)\/?/g).exec($window.location)[1];

  // Load the motdit
  $http.get('/api/v1/motsdits/' + motdit_id + '/?format=json').success(function(data) {
    $scope.motdit = data;
  });

  // Load all related motsdits
  $http.get('/api/v1/motsdits?format=json').success(function(data) {
    $scope.related = data;
  });

});
