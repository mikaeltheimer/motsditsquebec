/**
 * Filter controller
 * Handles all logic related to the filter, using filtering events
 */
angular.module('MotsDitsQuebec').controller('FilterCtrl', function($rootScope, $scope, $http, $window, $cookies, $log) {

  // Set the default filter
  $scope.active_category = {"id": 0, "name": "Toutes Categories"};
  $scope.active_subfilters = {};

  $scope.available_subfilters = {};
  $scope.categories = [$scope.active_category];
  $scope.hide_menus = false;

  // Set up a subfilter

  // Load the categories
  $http.get('/api/v1/categories/?format=json').success(function(data) {
    for(var i=0; i< data.count; i++) $scope.categories.push(data.results[i]);
  });

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
   * Choose a category to show
   */
  $scope.showCategory = function(category){

    $scope.hideMenus();

    // Emit the event
    $rootScope.$broadcast("categoryFilterEvent", category);

    // Set the active category

    // Set up the new filter
    $scope.active_category = category;
    $scope.active_subfilters = {};

    // Set up subfilters
    $scope.available_subfilters = {};

    // Populate the available subfilters
    angular.forEach($scope.active_category.subfilters, function(subfilter){
      if(!$scope.available_subfilters[subfilter.subfilter_type])
        $scope.available_subfilters[subfilter.subfilter_type] = {name: subfilter.subfilter_type, subfilters: []};
      $scope.available_subfilters[subfilter.subfilter_type].subfilters.push(subfilter);
    });

  };


  /**
   * Choose a subfilter to show
   * @TODO implement
   */
  $scope.setSubfilter = function(type, subfilter){

    $scope.active_subfilters[type] = subfilter;

    // Dispatch a subfilter event
    $rootScope.$broadcast("categorySubFilterEvent", {category: $scope.active_category, subfilters: $scope.active_subfilters});

  };

  /** 
   * Remove the active subfilter
   * @TODO implement
   */
  $scope.clearSubfilter = function(subfilter){
  };


});
