/**
 * Filter controller
 * Handles all logic related to the filter, using filtering events
 */
angular.module('MotsDitsQuebec').controller('FilterCtrl', function($rootScope, $scope, $http, $location, $window, $cookies, $log) {

  // Set the default filter
  $scope.active_category = {"id": 0, "name": "Toutes Categories"};
  $scope.active_subfilters = {};
  $scope.active_motdit = null;

  $scope.available_subfilters = {};
  $scope.categories = [$scope.active_category];
  $scope.hide_menus = false;

  $scope.ordering = '-recommendations';     // default to ordering by # recommendations DESC
  $scope.mon_reseau = false;                // default to everything

  var query_string = (function() {
      var q = $window.location.search.substr(1), qs = {};
      if (q.length) {
          var keys = q.split("&"), k, kv, key, val, v;
          for (k = keys.length; k--; ) {
              kv = keys[k].split("=");
              key = kv[0];
              val = decodeURIComponent(kv[1]);
              if (qs[key] === undefined) {
                  qs[key] = val;
              } else {
                  v = qs[key];
                  if (v.constructor != Array) {
                      qs[key] = [];
                      qs[key].push(v);
                  }
                  qs[key].push(val);
              }
          }
      }
      return qs;
  })();

  var initial_refresh = false;

  // Load the categories
  $http.get('/api/v1/categories/?format=json').success(function(data) {
    for(var i=0; i< data.count; i++) $scope.categories.push(data.results[i]);

      // Once categories are loaded, check if the filters need to be set

      initial_refresh = false;
      if(query_string.category){

        var queried_category;

        // Find the category
        angular.forEach($scope.categories, function(category){
          console.log(category.id, query_string.category);
          if(category.id == parseInt(query_string.category, 10)){
            activateCategory(category);
          }
        });

        // Find which subfilters to activate
        if($scope.active_category.subfilters){
          angular.forEach($scope.active_category.subfilters, function(subfilter){
            // Iterate over all queried subfilters
            angular.forEach(query_string.subfilters.split(','), function(subfilter_id){
              if(parseInt(subfilter_id, 10) == subfilter.id)
                $scope.active_subfilters[subfilter.subfilter_type] = subfilter;
            });
          });
        }
        initial_refresh = true;
      }


      if(query_string.ordering){
        $scope.ordering = query_string.ordering;
        initial_refresh = true;
      }

      refresh();

  });

  /**
   * Sets the active category and the related subfilters
   */
  var activateCategory = function(category){
    $scope.active_category = category;
    angular.forEach($scope.active_category.subfilters, function(subfilter){
      if(!$scope.available_subfilters[subfilter.subfilter_type])
        $scope.available_subfilters[subfilter.subfilter_type] = {name: subfilter.subfilter_type, subfilters: []};
      $scope.available_subfilters[subfilter.subfilter_type].subfilters.push(subfilter);
    });
  };

  /**
   * Sends a categoryFilter event to make all active feeds refresh
   */
  var refresh = function(){
    $rootScope.$broadcast("categoryFilterEvent", $scope.active_category, $scope.active_subfilters, $scope.ordering);
  };

  /**
   *
   */
  $scope.changeFilter = function(){
    $rootScope.$broadcast("filterChangedEvent", $scope.active_category, $scope.active_subfilters, $scope.ordering);
  };

  /**
   * Hides menus after changing category
   */
  $scope.hideMenus = function(){
    $scope.hide_menus = true;
    setTimeout(function(){
      $scope.$apply(function() {
        $scope.hide_menus = false;
      });
    }, 500);
  };

  /**
   * Changes the sort priority of the mots-dits
   */
  $scope.setOrdering = function(type){
    $scope.ordering = type;
    refresh();
  };

  /**
   * Choose a category to show
   */
  $scope.showCategory = function(category){

    $scope.hideMenus();

    // Reset subfilters
    $scope.active_subfilters = {};
    $scope.available_subfilters = {};
    activateCategory(category);

    // Send a refresh event to the application
    refresh();
    $scope.changeFilter();

  };


  /**
   * Choose a subfilter to show
   */
  $scope.setSubfilter = function(type, subfilter){

    $scope.active_subfilters[type] = subfilter;

    // Emit the event
    refresh();
    $scope.changeFilter();

  };

  /** 
   * Remove the active subfilter
   */
  $scope.clearSubfilter = function(subfilter){
    delete $scope.active_subfilters[subfilter.subfilter_type];

    // Emit the event
    refresh();
    $scope.changeFilter();
  };

  /**
   * Event to auto-set the filters (for the mots-dit view)
   */
  $scope.$on('setMotDitEvent', function(e, motdit){

    console.log("setting motdit");

    if(motdit.category){

      // @TODO: This checks every 0.1s to see if the categories are loaded, is there a better way?
      var setCategory = function(){
        if($scope.categories.length == 1) return setTimeout(setCategory, 100);
        $scope.$apply(function() {
          angular.forEach($scope.categories, function(category){
            if(category.id == motdit.category.id){
              activateCategory(category);
            }
          });
          angular.forEach(motdit.subfilters, function(subfilter){
            $scope.active_subfilters[subfilter.subfilter_type] = subfilter;
          });
        });
      };

      setTimeout(setCategory, 100);
    }
    $scope.active_motdit = motdit;
    refresh();
  });


});
