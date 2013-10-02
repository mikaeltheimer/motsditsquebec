
function MotsDitsCtrl($scope, $http) {

  $scope.motsdits = [];

  $http.get('/api/v1/motsdits/?format=json').success(function(data) {
    $scope.motsdits = data;
  });

  $scope.countMotsDits = function(){
    return $scope.motsdits.length;
  };

}