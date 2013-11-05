angular.module('MotsDitsQuebec').controller('HomepageCtrl', function($scope, $http, $window, $cookies) {

  $scope.motsdits = [];

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

  // Load a list of motdits
  $http.get('/api/v1/motsdits?format=json').success(function(data) {
    $scope.motsdits = data.results;
  });

  $scope.busy = false;

  var load_more = function(){
    console.log("TESTING");
    if ($scope.busy) return;
    $scope.busy = true;
    $http.get('/api/v1/motsdits?format=json').success(function(data) {
      // Add to scope
      for(var i=0; i<data.count; i++){
        $scope.motsdits.push(data.results[i]);
      }
      $scope.busy = false;
    });
  };

});
