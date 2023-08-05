(function() {
    'use strict';
    angular
        .module('portfolio.account')
        .run(appRun);
    appRun.$inject = [ 'routehelper' ];

    function appRun(routehelper) {
        routehelper.configureRoutes(getRoutes());
    }

    function getRoutes() {
        return [
            {
                url: '/',
                config: {
                    template: '<account-list></account-list>',
                    title: 'Account list',
                    settings: {
                        nav: 1,
                        content: '<i class="fa fa-dashboard"></i> Dashboard'
                    },
                }
            },
            {
                url: '/accounts/:id',
                config: {
                    template: '<account-detail></account-detail>',
                    title: 'Account details',
                    settings: {
                        nav: 1,
                        content: '<i class="fa fa-dashboard"></i> Dashboard'
                    },
                },
            },
        ];
    }
})();
