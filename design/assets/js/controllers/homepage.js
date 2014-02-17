angular.module('MotsDitsQuebec').controller('HomepageCtrl', function($scope, $http, $window, $cookies, $timeout, $log) {

  // Current active set of Mots-Dits + the filters that generated them
  $scope.motsdits = [];
  $scope.filters = {};

  // Pagination
  $scope.page = 1;
  $scope.per_page = 12;
  $scope.next_page = null;

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


  var pending_load_request;

  $scope.recommend = function(motdit){

    console.log('/api/v1/motsdits/' + motdit.slug + '/recommend/');

    $http.post('/api/v1/motsdits/' + motdit.slug + '/recommend/', {'recommend': true}).
      success(function(data){
        if(data.recommended){
          motdit.recommendations += 1;
        }else{
          motdit.recommendations -= 1;
        }
      }).
      error(function(data){
        console.log("Error recommending motdit");
    });
  };


  /**
   * Reloads mots-dits for the page
   */
  $scope.load_motsdits = function(handler){

    // Set up the filters
    var filters = $scope.filters;
    filters.page = $scope.page;
    filters.count = $scope.per_page;

    pending_load_request = $http.get('/api/v1/motsdits?' + serialize(filters) + '&format=json').success(function(data) {

      $scope.next_page = data.next;

      // If not handler specified, do a basic reload
      if(!handler)  $scope.motsdits = data.results;
      // Otherwise call the handler
      else          handler(data);
    });
  };

  // Catch a search event
  $scope.$on('motditSearchEvent', function(e, query){
    $scope.filters.search = query;
    $scope.load_motsdits();
  });

  // Infinite scroll
  $scope.busy = false;

  $scope.load_more = function(){
    if ($scope.busy || !$scope.next_page) return;
    $scope.page++;
    $scope.busy = true;
    $scope.load_motsdits(function(data) {
      // Add to scope
      for(var i=0; i<data.results.length; i++){
        $scope.motsdits.push(data.results[i]);
      }
      $scope.busy = false;
    });
  };

  var loaded_once = false;
  // Catch filter events
  $scope.$on('categoryFilterEvent', function(e, category, subfilters, ordering, search, geo){

    loaded_once = true;

    // Filter by category id
    if(category.id > 0) $scope.filters = {'category': category.id};
    // The special category 0 resets our filters
    else                $scope.filters = {};


    // Filter by subfilters
    subfilter_ids = [];

    angular.forEach(subfilters, function(subfilter){
      subfilter_ids.push(subfilter.id);
    });

    // Apply subfilters
    if(subfilter_ids) $scope.filters['with_subfilters'] = subfilter_ids.join();
    // Apply sort
    if(ordering) $scope.filters['order_by'] = ordering;
    // Apply search
    if(search) $scope.filters['search'] = search;
    // Apply geo
    if(geo) $scope.filters['geo'] = geo;

    // Reset the page
    $scope.page = 1;
    $scope.load_motsdits();
  });

});
