
(function () {
    'use strict';

    angular
        .module('portfolio.account')
        .directive('accountList', accountList);

    function accountList() {
        return {
            restrict: 'E',
            templateUrl: '/static/js/portfolio/components/account-list.directive.html',
            controller: 'AccountListDirectiveController',
            controllerAs: 'vm',
            transclude: true,
            bindToController: true
        };
    }

})();
