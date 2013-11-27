angular.module('MotsDitsQuebec').controller('OpinionModalCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  var motdit_id = (/mot\/([^\/\#\!]+)\/?/g).exec($window.location)[1];
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $scope.form = {};


  $scope.submit_form = function(){
    console.log("Submitting!");
    if(!$scope.form.opinion)
      return console.log("Can't submit...");

    console.log("Submitting opinion...");

    $scope.submit_disabled = true;

    $http.post('/api/v1/motsdits/' + motdit_id + '/opinions/', $scope.form).
      success(function(result){
        alert("Saved your motdit, redirecting to the page!");
        $window.location.href = "/mot/" + motdit_id;
      }).
      error(function(data, status){
        alert("Error saving mot-dit " + status);
        $scope.submit_disabled = false;
    });
  };

});
