/**
 * Positions
 * @namespaces portfolio.positions.services
 */

(function () {
    'use strict';

    angular
        .module('portfolio.positions.services')
        .factory('Positions', Positions);

    Positions.$inject = ['$http', '$resource', 'portfolioConfig',
                         '$timeout', 'logger'];

    /**
     * @
     * @desc
     */
    function Positions($http, $resource, portfolioConfig,
                       $timeout, logger) {
        var Positions = {
            all: all,
            google_quote: google_quote,
            market_value: market_value,
            yahoo_quote: yahoo_quote,
            google_local_quote: google_local_quote,
            getLivePrices: getLivePrices,
            securities: [],
            currencies: [],
            total_mktval: 0,
            total_day_change: 0,
            liveTimer: null
        };
        
        var securities_d = {};

        return Positions;

        /**
         * @name getLivePrices
         *
         */
        function getLivePrices(securities, currencies) {

            var i, delay, cumulative_delay = 0;
            var minTime = portfolioConfig.APIMinWaitTime;
            var maxTime = portfolioConfig.APIMinWaitTime;
            var refreshRate = 15; // minutes
            var ticker;

            Positions.securities = securities;
            Positions.currencies = currencies;
            for(i=0; i < securities.length; i++) {
                ticker = securities[i].ticker;
                if ( ticker === 'N/A' ) {
                    continue;
                }
                securities_d[ticker] = securities[i].name;
                delay = Math.random()*(maxTime-minTime+1)+minTime;
                cumulative_delay += delay;
                console.log(ticker, cumulative_delay, delay);
                /* call getQuoteForSecurity with 'ticker' argument */
                $timeout(getQuoteForSecurity,
                         cumulative_delay, true,
                         ticker, 'local');
            }

            Positions.liveTimer = $timeout(function () {
                getLivePrices(securities, currencies);
            }, refreshRate*60*1000);

        }

        function getQuoteForSecurity(ticker, provider) {
            /* Stupid workaround for lack of default parameters ... */
            provider  = (typeof provider !== 'undefined') ?
                provider : 'yahoo';
            /* Two possible providers for quote, Google and Yahoo */
            switch(provider) {
            case 'local':
                Positions.google_local_quote(ticker)
                    .then(positionsLiveSuccessLocalFn,
                          positionsLiveErrorLocalFn);
            }
        }
        function positionsLiveSuccessLocalFn(data) {
            if  (!data.data) {
                logger.warning("getQuote success: No data");
            }
            logger.debug('LiveSuccessLocal', data.data);
            var result = data.data;
            var ticker = result.ticker;
            var currency = result.currency;
            var price = result.price;
            var changePercentage = result.change_percentage;
            var change = result.change;
            var lastTrade = result.date;

            populateSecurityData(ticker, currency, price,
                                 changePercentage, change,
                                 lastTrade);
        }

        function positionsLiveErrorLocalFn(data) {
            console.log('GoogleLocal Failed', data);
        }

        function populateSecurityData(ticker, currency, price,
                                      changePercentage,
                                      change, lastTrade) {

            logger.debug('populateSecurityData called');
                        var securityName;
            var securityCurrency;
            var ltDateSecs;

            if (typeof Positions.positions === 'undefined') {
                /* It should be impossible to get here with
                   Positions.positions undefined, but just in case, do nothing  */
                ;
            }
            else {
                /* If ticker is not found, Yahoo returns null */
                if ( typeof ticker !== 'undefined' ||  ticker !== null) {
                    securityName = securities_d[ticker];
                    securityCurrency = currency;
                    fx.base = Positions.currencies['base'];
                    fx.rates = Positions.currencies.rates;
                    /*
                       Positions.positions has securities whose count is
                       greater than zero. However, Securities.all()
                       service returns all securities in DB. Hence
                       it is possible that Positions.positions[securityName]
                       is not defined
                    */
                    if ( typeof Positions.positions[securityName] !== 'undefined' ) {
                        /* l is latest value */
                        Positions.positions[securityName]['price'] = price;
                        Positions.positions[securityName]['change'] = change;
                        Positions.positions[securityName]['change_percentage'] = changePercentage;
                        /* parse return milliseconds, second wanted */
                        ltDateSecs = Date.parse(lastTrade) / 1000;
                        Positions.positions[securityName]['latest_date'] =
                            moment.unix(ltDateSecs).format('YYYY-MM-DD');
                        /* convert currency uned in security price
                           to base currency and use the converted
                           value as market value for the security in
                           question
                        */
                        Positions.positions[securityName]['mktval'] =
                            fx(Positions.positions[securityName]['price'] *
                               Positions.positions[securityName]['shares'])
                            .from(securityCurrency).to(fx.base);
                        Positions.positions[securityName]['day_change'] =
                            Positions.positions[securityName]['shares'] *
                            Positions.positions[securityName]['change'];
                        if (typeof Positions.positions[securityName]['day_change'] !== 'undefined') {
                            Positions.positions[securityName]['day_change'] =
                                fx(Positions.positions[securityName]['day_change'])
                                .from(securityCurrency)
                                .to(fx.base);
                        }
                        // Update market value & daily change
                        Positions.total_mktval = 0;
                        Positions.total_day_change = 0;
                        for (var position in Positions.positions) {
                            if (Positions.positions.hasOwnProperty(position)) {
                                Positions.total_mktval +=
                                    Positions.positions[position]['mktval'];
                                if (typeof Positions.positions[position]['day_change'] !== 'undefined') {
                                    Positions.total_day_change +=
                                        Positions.positions[position]['day_change'];
                                    console.log(Positions.positions[position]);
                                    console.log(Positions.positions[position]['day_change']);
                                }
                            }
                        }
                    }
                }
            }
        }
        /**
         * @name all
         *
         */
        function all(accountID) {
            return $http.get('/portfolio/api/v1/positions/' + accountID + '/')
                .then(allSuccessFn, allErrorFn);
        }

        function allSuccessFn(data) {
            logger.debug("allSuccessFn", data.data);
            Positions.positions = data.data;
            return data.data;
        }

        function allErrorFn(data) {
            logger.error("allErrorFn", data);
        }

        function google_quote(security) {
            var url = 'http://finance.google.com/finance/info?q=' + security;
            var quote = $resource('http://finance.google.com/finance/info', 
                                     {client:'ig', callback:'JSON_CALLBACK'},
                                     {get: {method:'JSONP', params:{q:security}, 
                                            isArray: true}});
            return quote.get().$promise;
        }

        function market_value(positions) {

            var position;
            var total = 0;

            for (position in positions) {
                if (positions.hasOwnProperty(position)) {
                    total += positions[position]['mktval'];
                }
            }
            return total;
        }
        
        function yahoo_quote(security) {
            var query = 'select * from yahoo.finance.quotes where symbol = "' + 
                    security + '"';
            var format = '&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=JSON_CALLBACK';
            var url = 'https://query.yahooapis.com/v1/public/yql?q=' +
                    encodeURIComponent(query) + '%0A%09%09' + format;
            return $http.jsonp(url);
        }

        /**
         * Google quote using local backend as proxy to prevent
         * No ‘Access-Control-Allow-Origin’ header is present on the
         * requested resource. Origin ‘xxx’ is therefore not allowed
         * access. Python's requests lib doesn't care if the header is
         * there or not, browser does.
         */
        function google_local_quote(security) {
            return $http.get('/portfolio/api/v1/' + security + '/quote/');
        }
    }
})();
