
function ExampleCtrl($scope, $http) {

  $scope.categories = [];

  $http.get('/api/v1/categories/?format=json').success(function(data) {
    $scope.categories = data;
  });

  $scope.numCategories = function(){
    return $scope.categories.length;
  };
 
  $scope.addTodo = function() {
    $scope.todos.push({text:$scope.todoText, done:false});
    $scope.todoText = '';
  };
 
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.todos, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };

}