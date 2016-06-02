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
            otdel_obj: '',
            configuration: '',
            status: 'all',
            important: '',
            tema: '',
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
                $scope.data.importants.unshift({id:'', name:'Все'});
                $scope.data.tems.unshift({id:'', name:'Все'});
                $scope.filters.otdel_obj = $scope.data.otdels[0];
            })
    }

    $scope.setStatus = function(status){
        $scope.filters.status = status;
    }

    $scope.setOtdel = function(otdel){
        $scope.filters.otdel = otdel.id;
        $scope.filters.otdel_obj = otdel;
        $scope.filters.configuration = "";
        $scope.filters.tema = "";
    }

    $scope.setConfig = function(config){
        $scope.filters.configuration = config;
        $scope.filters.tema = "";
    }

    $scope.setImportant = function(important){
        $scope.filters.important = important;
    }

    $scope.setTema = function(tema){
        $scope.filters.tema = tema;
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
    //Фильрация 1С конфигураций (при выборе отдела)
    $scope.filteredConfigur = function(otdel){
        return function(item){
            if(otdel.id){
                if(item.id){
                    search_item = findById(item.id, otdel.configuration_1c)
                    if(search_item){
                        return true;
                    }else{
                        false;
                    }
                }else{
                    return true;
                }
            }else{
                return true;
            }
        }
    }
    //Фильрация тем при изменении отдела
    $scope.filteredTemaByOtdel = function(otdel){
        return function(item){
            if(otdel.id){
                if(item.id){
                    search_item = findById(item.configuration_1c, otdel.configuration_1c)
                    if(search_item){
                        return true;
                    }else{
                        false;
                    }
                }else{
                    return true
                }
            }else{
                return true
            }
        }
    }

    $scope.filteredTemaByConfigur = function(configur){
        return function(item){
            if(configur){
                if(item.id){
                    if(item.configuration_1c == configur){
                        return true
                    }else{
                        return false
                    }
                }else{
                    return true
                }
            }else{
                return true
            }
        }
    }
    init()
})
