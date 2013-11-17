angular.module('MotsDitsQuebec').controller('EditMotditCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.categories = [];
  $scope.form = {subfilters: {}};

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

    // Enumerates subfilters by type to show all available subfilters properly
    angular.forEach($scope.categories, function(c, index){

      var subfilters = {};
      angular.forEach(c.subfilters, function(s){
        // ensure the array exists;
        if(!subfilters[s.subfilter_type]) subfilters[s.subfilter_type] = [];
        // push the subfilter into the new dict
        subfilters[s.subfilter_type].push(s);
      });

      console.log(subfilters);
      $scope.categories[index].assoc_subfilters = subfilters;

    });

    console.log($scope.categories[0]);

    $scope.form.category = $scope.categories[0];
  });

});
