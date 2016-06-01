var App = angular.module('app', [])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

App.controller('SupportCtrl', function($scope, $http){
    var init = function(){
        $scope.configurationC = '';

        $http.get('/')
            .then(function(response){
                $scope.data = response.data
                //$scope.data.user.otdel.configuration_1c.unshift({id: '', name:'Все'})
                console.log(response.data)
            })
    }

    init()
})