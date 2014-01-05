/**
 * Opinion Modal
 * Handles submission of new opinion/reviews for MotsDits
 */
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
        $scope.closeModal();
        $window.location.reload(false);
      }).
      error(function(data, status){
        alert("Error saving mot-dit " + status);
        $scope.submit_disabled = false;
    });
  };

  $scope.closeModal = function(){ $rootScope.$broadcast("closeModal", {}); };

});
