angular.module('MotsDitsQuebec').controller('EditMotditCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.categories = [];
  $scope.form = {};

  $scope.preload_image = function(el) {

    var image = el.files[0];
    var formData = new FormData();
    formData.append('image', image, image.name);

    console.log("Uploading... " + image.name);

    $http.post('/api/v1/photos/upload/tmp', formData, {
        headers: {'Content-Type': undefined },
        transformRequest: angular.identity
    }).success(function(result) {
        // Set the value of the photo
        $scope.form.photo = result.src;
        console.log($scope.form.photo);
    });
  };

  $scope.submit_form = function(){
    console.log("Submitting a new mot-dit...");
    $http.post('/api/v1/motsdits/new', $scope.form).success(function(result){
      console.log('Success!!');
    });
  };

  // Load the categories list
  $http.get('/api/v1/categories/').success(function(response){
    $scope.categories = response.results;
    $scope.form.category = $scope.categories[0];
  });

});
