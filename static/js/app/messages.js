var App = angular.module('app', [])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

App.controller('MessagesCtr', function($scope, $http, $interval){
    var init = function(){
        $scope.userMessage = "";
        $http.get('')
            .then(function(response){
                $scope.messages = response.data.messages
                $scope.support = response.data.support;
                polling();
            })
    }

    var polling = function(){
            var lastID = $scope.messages[$scope.messages.length-1].id;
            $http.post('/proposal/polling/' + $scope.support + '/', {lastID: lastID})
                .then(function(response){
                    messages = response.data.messages
                    if(messages.length){
                        angular.forEach(messages, function(message){
                            $scope.messages.push(message);
                        })
                    }
                    polling()
                })
    }
    $scope.sendMessage = function(){
        if($scope.userMessage.length){
            $http.post('', {message: $scope.userMessage, action: "addMessage"})
                .then(function(response){
                    //$scope.messages.push(response.data.message)
                    $scope.userMessage = ""
                })
        }else{
            alert('Введите сообщение!')
        }
    }

    init()
})
