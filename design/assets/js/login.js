angular.module('MotsDitsQuebec').controller('LoginCtrl', function($scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

  $scope.doLogin = function(){
    $http.post('/api/auth/login/?format=json', {'email': this.email, 'password': this.password}).success(function(data) {
      $scope.response = data;
      if($scope.response.isLogged){
        $window.location.href = "/";
      }else{
        alert("Could not log you in!");
      }
    });
  };

});
