angular.module('MotsDitsQuebec').controller('FeedCtrl', function($scope, $http, $window, $cookies, $timeout, $log) {

  // Current active set of Activities + the filters that generated them
  $scope.activities = [];
  $scope.filters = {};

  // Pagination
  $scope.page = 1;
  $scope.per_page = 12;
  $scope.next_page = null;

  $scope.date_reported = null;
  $scope.active_user = null;

  try {
    var username = (/feed\/([^\/\#\!]+)\/?/g).exec($window.location)[1];
    $http.get('/api/v1/users/' + username).success(function(data){
      $scope.active_user = data;
      console.log($scope.active_user);
    });
  } catch(err){
    // Do nothing
  }

  // Set up the request to ensure we can access resources
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  /**
   * Helper function, serializes objects to query components
   */
  var serialize = function(obj) {
    var str = [];
    for(var p in obj)
       str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    return str.join("&");
  };

  var months = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'];
  var days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];

  /**
   * Reloads activities for the page
   */
  $scope.load_activities = function(handler){

    // Set up the filters
    var filters = $scope.filters;
    filters.page = $scope.page;
    filters.count = $scope.per_page;

    if(username) filters.created_by = username;

    $http.get('/api/v1/activities?' + serialize(filters) + '&format=json').success(function(data) {

      $scope.next_page = data.next;

      if(!handler){
        $scope.activities = [];
        for(var i=0; i<data.results.length; i++){

          var d = new Date(data.results[i].created);

          if(!$scope.date_reported || d.getDate() != $scope.date_reported.getDate()){

            $scope.activities.push({
              'type': 'DateMarker',
              'day': days[d.getDay()],
              'date': d.getDate(),
              'month': months[d.getMonth()],
              'year': d.getYear() + 1900
            });

            $scope.date_reported = d;
          }

          $scope.activities.push(data.results[i]);
        }
      // Handler allows full override
      }else return handler(data);
    });
  };


  // Infinite scroll
  $scope.busy = false;

  $scope.load_more = function(){
    if ($scope.busy || !$scope.next_page) return;
    $scope.page++;
    $scope.busy = true;
    $scope.load_activities(function(data) {
      // Add to scope
      for(var i=0; i<data.results.length; i++){
        $scope.activities.push(data.results[i]);
      }
      $scope.busy = false;
    });
  };


  // Catch filter events
  $scope.$on('categoryActivityFilterEvent', function(e, category){
    console.log("Filtering to show only activities from category " + category.name);
    // Filter by category id
    if(category.id > 0) $scope.filters = {'category__id': category.id};
    // The special category 0 resets our filters
    else                $scope.filters = {};

    // Reset the page
    $scope.page = 1;

    $scope.load_activities();
  });


  // Load a list of activities
  $scope.load_activities();


});
