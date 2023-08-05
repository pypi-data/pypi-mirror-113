(function () {
    'use strict';

    angular
        .module('portfolio.account')
        .controller('AccountListDirectiveController', AccountListDirectiveController);

    AccountListDirectiveController.$inject = ['$q', 'Accounts', 'logger'];

    function AccountListDirectiveController($q, Accounts, logger) {
        var vm = this;

        activate();

        function activate() {
            /* Get list of accounts */
            var promises = [getAccounts()];
            return $q.all(promises).then(function() {
                logger.info('accounts list controller activated');
            });
        }

        function getAccounts() {
            return Accounts.all().then(function(data) {
                console.log(data);
                vm.accounts = data.data;
            });
        }
    }
})();
