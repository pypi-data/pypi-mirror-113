(function () {
    'use strict';

    angular
        .module('portfolio.account')
        .directive('accountDetail', accountDetail);

    function accountDetail() {
        return {
            restrict: 'E',
            templateUrl: '/static/js/portfolio/components/account-detail.directive.html',
            controller: 'AccountDetailDirectiveController',
            controllerAs: 'vm',
            transclude: true,
            bindToController: true
        };
    }

})();
