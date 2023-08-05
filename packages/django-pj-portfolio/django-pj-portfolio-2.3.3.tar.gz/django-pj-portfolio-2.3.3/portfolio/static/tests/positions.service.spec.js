(function () {
    'use strict';

    describe('Positions service', function () {
        var $httpBackend, Positions, $rootScope, $timeout, $q;
        var logger;
        var googleQuoteTicker = 'WSR';
        var yahooQuoteTicker = 'WSR';

        var positionJSON = 'positions_detail.json';

        beforeEach(function() {
            module('portfolio');
            module('portfolio.templates');
        });

        beforeEach(inject(function($controller, _$rootScope_,
                                   _$httpBackend_, _Positions_, _$timeout_, _$q_,
                                   _logger_) {

            /* Fixtures get cached. In case other tests are changing the
               cache, remove  it.. and reload later
            */
            var fixtures = loadJSONFixtures(positionJSON);
            delete fixtures[positionJSON];

            $httpBackend = _$httpBackend_;
            Positions = _Positions_;
            $rootScope = _$rootScope_;
            $timeout = _$timeout_;
            $q = _$q_;
            logger = _logger_;

            jasmine.getJSONFixtures().fixturesPath='base/portfolio/static/tests/mock';
            spyOn(Positions, 'google_local_quote').and.callFake(function(ticker) {
                console.log('local quote mock', ticker);
                return $q.when( { data: getJSONFixture(ticker.toLowerCase() + '_quote.json')});
            });

        }));

        it('should get quote from Google', function() {
            var response;

            $httpBackend.expectJSONP('http://finance.google.com/finance/info?callback=JSON_CALLBACK&client=ig&q=' + googleQuoteTicker)
                .respond(getJSONFixture('google_quote.json'));

            Positions.google_quote(googleQuoteTicker).then(function(data){
                response = data;
            }, function(data) {
                console.log('google_quote error ', data);
            });
            $httpBackend.flush();
            expect(response[0]['t']).toEqual(googleQuoteTicker);
        });

        it('should get quote from Yahoo', function() {
            var response;
            var query = 'select * from yahoo.finance.quotes where symbol = "' + 
                    yahooQuoteTicker + '"';
            var format = '&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=JSON_CALLBACK';
            var url = 'https://query.yahooapis.com/v1/public/yql?q=' +
                    encodeURIComponent(query) + '%0A%09%09' + format;

            $httpBackend.expectJSONP(url).respond(getJSONFixture('yahoo_quote.json'));
            Positions.yahoo_quote(yahooQuoteTicker).then(function(data){
                response = data;
            }, function(data) {
                console.log('google_quote error ', data);
            });
            $httpBackend.flush();
            expect(response.data.query.results.quote.Symbol).toEqual(yahooQuoteTicker);
        });

        it('should have some results', function() {
            var result;

            $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
                .respond(getJSONFixture('positions_detail.json'));

            Positions.all('1').then(function () {

                result = Positions.positions;
                expect(result['Whitestone REIT'].price).toEqual(14.0);
            }, function(data) {
                console.log("Error", data);
            });

            $httpBackend.flush();
        });

        it('should calculate market value correctly', function() {

            var positions;
            var mktval;

            $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
                .respond(getJSONFixture(positionJSON));

            Positions.all('1').then(function () {
                positions = Positions.positions;
            }, function(data) {
                console.log("Error", data);
            });

            $httpBackend.flush();

            mktval = Positions.market_value(positions);

            /* Value will be in 'native' currency, no conversion to EUR done */
            expect(mktval).toBeCloseTo(49086.12, 2);

        });

        it('should get live prices and calculate total market value', function() {
            var securities = getJSONFixture('securities.json');
            var currencies = getJSONFixture('currencies.json');
            $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
                .respond(getJSONFixture(positionJSON));

            Positions.all('1').then(function() {
                ;
            });

            $httpBackend.flush();

            /* Start the loop for getting live prices. In the end we have
             * market value calculated with received prices */
            Positions.getLivePrices(securities, currencies);
            /* Stop timers */
            $timeout.flush();
            $timeout.cancel(Positions.liveTimer);
            $timeout.flush();

            /* Positions.market_value above gives different result as it's
             * been given static result where market values for different
             * securities have already been calculated, using currency
             * rates at a time. Those rates are differrent from the rates
             * used in this test
             */
            expect(Positions.total_mktval).toBeCloseTo(49093.82, 2);
        });
    });
})();
