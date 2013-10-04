var MDQ = angular.module('MotsDitsQuebec', ['ngCookies']);

MDQ.controller('LoginCtrl', function($scope, $http, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.response = {};

  $scope.doLogin = function(){
    $http.post('/api/auth/login/?format=json', {'username': 'stephen', 'password': 'goose'}).success(function(data) {
      $scope.response = data;
      if($scope.response[1].isLogged){
        $window.location.href = "/";
      }else{
        console.log("error");
      }
    });
  };

});