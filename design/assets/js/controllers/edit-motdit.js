angular.module('MotsDitsQuebec').controller('EditMotditCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.categories = [];
  $scope.subfilters = {};

  //$scope.image_url = null;

  $scope.preload_image = function(el) {

    var image = el.files[0];
    var formData = new FormData();
    formData.append('image', image, image.name);

    console.log("Uploading... " + image.name);

    $http.post('/api/v1/photos/upload/tmp', formData, {
        headers: { 'Content-Type': false },
        transformRequest: angular.identity
    }).success(function(result) {
        $scope.image_url = result.src;
        console.log($scope.image_url);
    });
  };

  // Load the categories list
  $http.get('/api/v1/categories/').success(function(response){
    $scope.categories = response.results;
    $scope.category = $scope.categories[0];
  });

  // @TODO: Load all the subfilters

});
