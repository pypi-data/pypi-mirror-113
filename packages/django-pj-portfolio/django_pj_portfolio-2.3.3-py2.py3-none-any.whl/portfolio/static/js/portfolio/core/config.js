(function() {
    'use strict';


    var core = angular.module('portfolio.core');

    core.config(configure);

    configure.$inject = [ '$routeProvider', 'routehelperConfigProvider',
                          '$logProvider', '$provide'];
    function configure($routeProvider,
                       routehelperConfigProvider, $logProvider,
                       $provide) {
        // if (hmiconfig.isProduction) {
        //     $logProvider.debugEnabled(false);

        //     $provide.decorator('$log', ['$delegate', function ($delegate) {
        //         $delegate.info = angular.noop;
        //     }]);
        //     $provide.decorator('$log', ['$delegate', function ($delegate) {
        //         $delegate.warn = angular.noop;
        //         return $delegate;
        //     }]);
        //     $provide.decorator('$log', ['$delegate', function ($delegate) {
        //         $delegate.error = angular.noop;
        //         return $delegate;
        //     }]);
        // }
        // else {
        //     $logProvider.debugEnabled(true);
        // }
        // Configure the common route provider
        routehelperConfigProvider.config.$routeProvider = $routeProvider;
        var resolveAlways = {
            // currentSettings: ['HMISettings' , function(HMISettings) {
            //     return HMISettings.getSettings();
            // }],
            // ahus: ['HMIAhusService', function(HMIAhusService) {
            //     return HMIAhusService.getSaved();
            // }]
        };
        routehelperConfigProvider.config.resolveAlways = resolveAlways;
    }
})();
