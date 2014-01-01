angular.module('MotsDitsQuebec').controller('PhotoModalCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.submit_disabled = true;
  $scope.form = {};

  // Pull the motdit from the URL
  var motdit_id = (/mot\/([^\/\#\!]+)\/?/g).exec($window.location)[1];

  $scope.preload_image = function(el) {

    var image = el.files[0];
    var formData = new FormData();
    formData.append('image', image, image.name);

    console.log("Uploading... " + image.name);

    $scope.submit_disabled = true;

    $http.post('/api/v1/photos/upload/tmp', formData, {
        headers: {'Content-Type': undefined },
        transformRequest: angular.identity
    }).success(function(result) {
        // Set the value of the photo
        $scope.form.photo = result.src;
        $scope.submit_disabled = false;
    });
  };

  $scope.submit_form = function(){
    console.log("Submitting!");
    if($scope.submit_disabled)
      return console.log("Can't submit...");

    console.log("Submitting photo...");

    $scope.submit_disabled = true;

    $http.post('/api/v1/motsdits/' + motdit_id + '/photos/', $scope.form).
      success(function(result){
        $scope.closeModal();
        $window.location.href = "/mot/" + motdit_id;
      }).
      error(function(data, status){
        alert("Error saving mot-dit " + status);
        $scope.submit_disabled = false;
    });
  };

  $scope.closeModal = function(){ $rootScope.$broadcast("closeModal", {}); };

});
