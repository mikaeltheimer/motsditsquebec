angular.module('MotsDitsQuebec').controller('EditMotditCtrl', function($rootScope, $scope, $http, $window, $cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  $scope.categories = [];
  $scope.form = {subfilters: {}};

  $scope.submit_disabled = true;

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

    if($scope.submit_disabled)
      return console.log("Can't submit...");

    $scope.form.subfilters = $scope.selected_subfilters;

    $scope.submit_disabled = true;

    $http.post('/api/v1/motsdits/new', $scope.form).
      success(function(result){
        $window.location.href = "/mot/" + result.motdit.slug;
      }).
      error(function(data, status){
        alert("Error saving mot-dit " + status);
        $scope.submit_disabled = false;
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
      $scope.categories[index].assoc_subfilters = subfilters;

    });

    $scope.form.category = $scope.categories[0];
    $scope.submit_disabled = false;
  });

  // Subfilters!
  $scope.selected_subfilters = {};

  // toggle selected_subfilters for a given filter
  $scope.toggleSelection = function(type, subfilter) {

    if(!$scope.selected_subfilters[type])
        $scope.selected_subfilters[type] = [];
    var idx = $scope.selected_subfilters[type].indexOf(subfilter);

    // is currently selected
    if (idx > -1) {
      $scope.selected_subfilters[type].splice(idx, 1);
    }

    // is newly selected
    else {
      $scope.selected_subfilters[type].push(subfilter);
    }
  };

});
