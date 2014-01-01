
angular.module('MotsDitsQuebec').controller('MotDitCtrl', function($rootScope, $scope, $http, $window, $cookies, $timeout) {

  // Pull the motdit from the URL
  var motdit_id = (/mot\/([^\/\#\!]+)\/?/g).exec($window.location)[1];

  $scope.content_view = "reviews";

  // Motdit data
  $scope.motdit = {};
  // Motdit reviews
  $scope.reviews = [];
  // Related objects
  $scope.related = [];

  $scope.modals = {};

  // Vote on an opinion
  $scope.vote = function(opinion, approve){
    $http.post('/api/v1/opinions/' + opinion.id + '/vote/', {'approve': approve}).
      success(function(data){
        console.log("Vote accepted!");
        opinion.user_vote = approve;
      }).
      error(function(data){
        console.log("Error registering vote...");
      });
  };

  // Like the currently displaying photo (presently uses top_photo)
  $scope.like_photo = function(photo){
    var new_state = !photo.user_likes;

    $http.post('/api/v1/photos/' + photo.id + '/like/', {'like': new_state}).
      success(function(data){
        console.log("Photo like swapped!");
        photo.user_likes = new_state;
      }).
      error(function(data){
        console.log("Error registering vote...");
    });

  };

  $scope.recommend = function(){

    var new_state = !$scope.motdit.user_recommends;

    console.log('/api/v1/motsdits/' + motdit_id + '/recommend/');

    $http.post('/api/v1/motsdits/' + motdit_id + '/recommend/', {'recommend': new_state}).
      success(function(data){
        if(data.recommended){
          console.log("Recommended motdit!");
          $scope.motdit.recommendations += 1;
          $scope.motdit.user_recommends = true;
        }else{
          console.log("Un-recommended motdit!");
          // @TODO: actually remove what we don't want to have in there
          $scope.motdit.recommendations -= 1;
          $scope.motdit.user_recommends = false;
        }
      }).
      error(function(data){
        console.log("Error recommending motdit");
    });
  };

  // Load the motdit
  $http.get('/api/v1/motsdits/' + motdit_id + '/?format=json').success(function(data) {
    // Send a filters event
    $scope.motdit = data;

    var max_weight = 0;
    angular.forEach($scope.motdit.tags, function(tag){ max_weight = max_weight < tag.weight ? tag.weight : max_weight;});

    // Set the sizing on each tag
    var max_size = 40;
    angular.forEach($scope.motdit.tags, function(tag){
      tag.size = max_size * (tag.weight / max_weight);
      if(tag.size > max_size){
        tag.size = max_size;
      }
      tag.size = tag.size + 'px';
    });

    $rootScope.$broadcast("setMotDitEvent", $scope.motdit);
  });

  // Load all related motsdits
  $http.get('/api/v1/motsdits?format=json').success(function(data) {
    $scope.related = data.results;
  });

  // Load reviews
  $http.get('/api/v1/motsdits/' + motdit_id + '/opinions/?format=json').success(function(data) {
    $scope.reviews = data.results;
  });

  // Redirect when categories change
  $scope.$on('filterChangedEvent', function(e, category, subfilters, ordering){

    subfilter_ids = [];
    angular.forEach(subfilters, function(subfilter){ subfilter_ids.push(subfilter.id); });
    $window.location.href = "/?category=" + category.id + "&subfilters=" + subfilter_ids.join() + "&ordering=" + ordering;
  });

  var clearModals = function(){
    // Clear all modals
    angular.forEach($scope.modals, function(value, key){
      $scope.modals[key] = false;
    });
  };

  $scope.$on('closeModal', clearModals);

  $scope.toggleModal = function(name){

    clearModals();
    $scope.modals[name] = !$scope.modals[name];
  };

});
