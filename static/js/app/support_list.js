var App = angular.module('app', [])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers
                       .common['X-Requested-With'] = 'XMLHttpRequest';

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

App.controller('SupportListCtrl', function($scope, $http){
    var init = function(){
        $scope.filters = {
            otdel: '',
            configuration: '',
            status: 'all',
            search : {
                otdel : '',
                configuration : ''
            }
        }

        $http.get('')
            .then(function(response){
                console.log(response.data)
                $scope.data = response.data
                $scope.data.otdels.unshift({id:'', name:'Все'});
                $scope.data.configurations.unshift({id:'', name:'Все'});
            })
    }

    $scope.setStatus = function(status){
        $scope.filters.status = status;
    }

    $scope.setOtdel = function(otdel){
        $scope.filters.otdel = otdel;
        $scope.filters.configuration = "";
    }

    $scope.setConfig = function(config){
        $scope.filters.configuration = config;
    }

    var findById = function(id, items){
        var result = false;

        angular.forEach(items, function(item){
            if(item.id == id){
                result = item;
            }
        })

        return result;
    }

    //фильрация по статусу
    $scope.filteredStatus = function(status){
        return function(item){
            switch (status) {
                case 'all' :
                    return true;

                    break;

                case 'active':
                    if (item.status.id == 3 || item.status.id == 2){
                        return true
                    }else{
                        return false
                    }
                    break;

                case 'close':
                    if(item.status.id == 4){
                        return true;
                    }else{
                        return false;
                    }

                    break;
            }
        }
    }

    $scope.filteredConfigur = function(otdel){
        return function(item){
            otdel = findById(otdel , $scope.data.otdels);
            console.log(otdel, item)
            if(otdel.id){
                if(item.id){
                    search_item = findById(item.id, otdel.configuration_1c)
                    //console.log(search_item)
                    if(search_item){
                        return true
                    }else{
                        false
                    }
                }else{
                    return true;
                }
            }else{
                return true;
            }
        }
    }

    init()
})
