
angular.module('MotsDitsQuebec').controller('MotDitCtrl', function($scope, $http, $window, $cookies, $timeout) {

  // Motdit data
  $scope.motdit = {};
  // Motdit reviews
  $scope.reviews = [];
  // Related objects
  $scope.related = [];

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

  // Pull the motdit from the URL
  var motdit_id = (/mot\/([^\/]+)\/?/g).exec($window.location)[1];

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
