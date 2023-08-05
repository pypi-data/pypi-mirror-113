(function () {
    'use strict';

    describe('AccountDetailDirectiveController', function() {

        var ctrl;
        var $rootScope, $q, $timeout, $httpBackend;
        var deferreds =  {};
        var Positions, Securities, Accounts, Currencies;
        var vm;
        var mockedMarketValue = 103.5;
        var mockedDayChange = 1.3;

        function resolvePromises() {
            /* Resolve the promises */

            deferreds.Securities.all.resolve({
                data: getJSONFixture('securities.json')
            });

            deferreds.Accounts.all.resolve({
                data: getJSONFixture('positions_detail.json')
            });

            deferreds.Currencies.all.resolve({
                data: getJSONFixture('currencies.json')
            });

            /* Promises are processed upon each digest cycle.
               Do that now
            */
            $rootScope.$digest();

            /* getLivePrices will call itself after timer has been expired.
               Cancel that timer to prevent that from happening
            */
            $timeout.cancel(Positions.liveTimer);

            /* flush the timers */
            $timeout.flush();
        }

        beforeEach(function () {
            module('portfolio');
            module('portfolio.templates');

            inject(function($controller, _$rootScope_, _$q_, _$timeout_,
                            _$httpBackend_, $location, _Positions_) {

                $rootScope = _$rootScope_;
                $q = _$q_;
                $timeout = _$timeout_;
                $httpBackend = _$httpBackend_;
                Positions = _Positions_;

                deferreds.Securities = {
                    all: $q.defer()
                };

                deferreds.Accounts = {
                    all: $q.defer()
                };

                deferreds.Currencies = {
                    all: $q.defer()
                };

                jasmine.getJSONFixtures()
                    .fixturesPath='base/portfolio/static/tests/mock';


                Securities = {
                    all: jasmine.createSpy('Securities', ['all'])
                        .and.returnValue(deferreds.Securities.all.promise)
                };

                Accounts = {
                    all: jasmine.createSpy('Accounts', ['all'])
                        .and.returnValue(deferreds.Accounts.all.promise)
                };

                Currencies = {
                    all: jasmine.createSpy('Currencies', ['all'])
                        .and.returnValue(deferreds.Currencies.all.promise)
                };

                spyOn(Positions, 'getLivePrices').and.callFake(function() {
                    Positions.total_mktval = mockedMarketValue;
                    Positions.total_day_change = mockedDayChange;
                    $q.when();
                });
                spyOn(Positions, 'all').and.callFake(function() {
                    Positions.positions = getJSONFixture('positions_detail.json');
                    $q.when();
                });
                vm = $controller('AccountDetailDirectiveController', {
                    $rootScope: $rootScope,
                    Positions: Positions,
                    Securities: Securities,
                    Accounts: Accounts,
                    Currencies: Currencies,
                    $timeout: $timeout
                });

            });
        });

        afterEach(function() {
            $timeout.verifyNoPendingTasks();
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should have controller defined', function() {

            resolvePromises();
            expect(vm).toBeDefined();
        });

        it('should have Positions defined', function() {

            resolvePromises();
            expect(vm.positions['Whitestone REIT']['price']).toBeDefined();
        });

        it('should have market value defined', function() {

            resolvePromises();
            expect(vm.total_mktval).toEqual(mockedMarketValue);
        });

        it('should have daily change defined', function() {

            resolvePromises();
            expect(vm.total_day_change).toEqual(mockedDayChange);
        });

        it('should kick off price updates', function() {

            resolvePromises();
            expect(Positions.getLivePrices).toHaveBeenCalled();
        });
    });
})();
