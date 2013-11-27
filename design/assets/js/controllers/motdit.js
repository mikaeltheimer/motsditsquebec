
angular.module('MotsDitsQuebec').controller('MotDitCtrl', function($scope, $http, $window, $cookies, $timeout) {

  // Pull the motdit from the URL
  var motdit_id = (/mot\/([^\/\#\!]+)\/?/g).exec($window.location)[1];

  // Motdit data
  $scope.motdit = {};
  // Motdit reviews
  $scope.reviews = [];
  // Related objects
  $scope.related = [];

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
          $scope.motdit.recommendations.unshift(data.user);
          $scope.motdit.user_recommends = true;
        }else{
          console.log("Un-recommended motdit!");
          // @TODO: actually remove what we don't want to have in there
          $scope.motdit.recommendations.shift();
          $scope.motdit.user_recommends = false;
        }
      }).
      error(function(data){
        console.log("Error recommending motdit");
    });
  };

  // Load the motdit
  $http.get('/api/v1/motsdits/' + motdit_id + '/?format=json').success(function(data) {
    $scope.motdit = data;
  });

  // Load all related motsdits
  $http.get('/api/v1/motsdits?format=json').success(function(data) {
    $scope.related = data.results;
  });

  // Load reviews
  $http.get('/api/v1/motsdits/' + motdit_id + '/opinions/?format=json').success(function(data) {
    $scope.reviews = data.results;
  });

});
