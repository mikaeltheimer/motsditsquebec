/**
 * Filter controller
 * Handles all logic related to the filter, using filtering events
 */
angular.module('MotsDitsQuebec').controller('FilterCtrl', function($rootScope, $scope, $http, $window, $cookies, $log) {

  // Set the default filter
  $scope.active_category = {"id": 0, "name": "Toutes Categories"};
  $scope.categories = [$scope.active_category];

  // Set up a subfilter

  // Load the categories
  $http.get('/api/v1/categories/?format=json').success(function(data) {
    for(var i=0; i< data.count; i++) $scope.categories.push(data.results[i]);
  });

  /**
   * Choose a category to show
   */
  $scope.showCategory = function(category){
    // Emit the event
    $rootScope.$broadcast("categoryFilterEvent", category);

    for(var i=0; i < $scope.categories.length; i ++){
      if($scope.categories[i].id == category.id){
        $scope.active_category = $scope.categories[i];
      }
    }
  };

  /**
   * Choose a subfilter to show
   * @TODO implement
   */
  $scope.setSubfilter = function(subfilter){
  };

  /** 
   * Remove the active subfilter
   * @TODO implement
   */
  $scope.clearSubfilter = function(subfilter){
  };


});
