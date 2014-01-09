/**
 * Profile photo modal
 * Handles changing of user profile photos
 * @TODO: Generalize the preload_image functionality
 */
angular.module('MotsDitsQuebec').controller('ProfilePhotoModalCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  try {
    $scope.form = {
      'user_id': (/feed\/([^\/\#\!]+)\/?/g).exec($window.location)[1]
    };
  } catch(err){
    $scope.form = {};
  }

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

    $http.post('/api/v1/profile_photo', $scope.form).
      success(function(result){
        $scope.closeModal();
        $window.location.reload(false);
      }).
      error(function(data, status){
        alert("Error saving photo " + status);
        $scope.submit_disabled = false;
    });
  };

  $scope.closeModal = function(){ $rootScope.$broadcast("closeModal", {}); };
});
