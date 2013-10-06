var MDQRegister = angular.module('MotsDitsQuebec', ['ngCookies']);

MDQRegister.controller('RegisterCtrl', function($scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.response = {};

  $scope.doRegister = function(){
    message = {
      'firstname': this.firstname,
      'lastname': this.lastname,
      'email': this.email,
      'username': this.username,
      'password': this.password,
      'password2': this.password2,
      'website': this.website
    };
    console.log(message);
    $http.post('/api/auth/register/?format=json', message).success(function(data) {
      $scope.response = data;
      if($scope.response.created){
        $window.location.href = "/register/success/";
      }else{
        alert("Registration failed!");
      }
    });
  };

});