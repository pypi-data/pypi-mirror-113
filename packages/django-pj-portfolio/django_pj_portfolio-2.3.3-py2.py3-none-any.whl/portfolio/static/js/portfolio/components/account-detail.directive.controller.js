(function () {
    'use strict';

    angular
        .module('portfolio.account')
        .controller('AccountDetailDirectiveController',
                    AccountDetailDirectiveController);

    AccountDetailDirectiveController.$inject = ['$q', 'logger',
                                        '$location', 'Positions', 'Securities',
                                        'Currencies', 'portfolioConfig',
                                        '$timeout', '$routeParams'];

    function AccountDetailDirectiveController($q, logger,
                                      $location, Positions, Securities,
                                      Currencies, portfolioConfig,
                                      $timeout, $routeParams) {

        var vm = this;

        vm.sortReverse = false;
        vm.sortColumn = '$key';

        /* 
           For now, Securities.all() returns an array, dictionary needed to
           be able to easily map ticker to name
        */
        vm.securities_d = {};

        vm.Positions = Positions;

        activate();

        /**
         * @name activate
         * @desc 
         * @memberOf portfolio.account.AccountDetailDirectiveController
         */

        function activate() {

            /* Get the account id from URL */
            var accountID = $routeParams.id;
            logger.info($location.path() + ' ' + accountID);
            /* Get list of accounts */
            var promises = {
                positions: Positions.all(accountID),
                securities: Securities.all(),
                currencies: Currencies.all()
            };
            vm.$onDestroy = cancelLiveTimer;

            return $q.all(promises).then(promisesSuccessFn, promisesErrorFn);

            function promisesSuccessFn(data, status, headers, config) {
                vm.positions = Positions.positions;
                vm.securities = Securities.securities;
                vm.currencies = data.currencies.data;
                logger.debug('accounts detail controller activated');
                logger.debug('Positions', vm.positions);
                logger.debug('Securities', vm.securities);
                logger.debug('Currencies', data.currencies);
                Positions.getLivePrices(vm.securities, vm.currencies);
            }

            function promisesErrorFn(data, status, headers, config) {
                logger.error('AccountDetailController: promisesErrorFn', data);
            }

            function cancelLiveTimer() {
                logger.debug('Timer destroy');
                $timeout.cancel(Positions.liveTimer);
            }
        }
    }
})();
