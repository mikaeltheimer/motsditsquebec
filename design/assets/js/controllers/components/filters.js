/**
 * Filter controller
 * Handles all logic related to the filter, using filtering events
 */
angular.module('MotsDitsQuebec').controller('FilterCtrl', function($rootScope, $scope, $http, $window, $cookies, $log) {

  // Set the default filter
  $scope.active_category = {"id": 0, "name": "Toutes Categories"};
  $scope.active_subfilters = {};
  $scope.active_motdit = null;

  $scope.available_subfilters = {};
  $scope.categories = [$scope.active_category];
  $scope.hide_menus = false;

  $scope.ordering = '-recommendations';     // default to ordering by # recommendations DESC
  $scope.mon_reseau = false;                // default to everything

  // Load the categories
  $http.get('/api/v1/categories/?format=json').success(function(data) {
    for(var i=0; i< data.count; i++) $scope.categories.push(data.results[i]);
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

  };


  /**
   * Choose a subfilter to show
   */
  $scope.setSubfilter = function(type, subfilter){

    $scope.active_subfilters[type] = subfilter;

    // Emit the event
    refresh();

  };

  /** 
   * Remove the active subfilter
   */
  $scope.clearSubfilter = function(subfilter){
    delete $scope.active_subfilters[subfilter.subfilter_type];
    // Emit the event
    refresh();
  };

  /**
   * Event to auto-set the filters (for the mots-dit view)
   */
  $scope.$on('setMotDitEvent', function(e, motdit){

    if(motdit.category){
      activateCategory(motdit.category);
      angular.forEach(motdit.subfilters, function(value){
        $scope.active_subfilters[value.type] = value;
      });
    }
    $scope.active_motdit = motdit;
    refresh();
  });


});
