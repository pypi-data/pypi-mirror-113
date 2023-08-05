.. :changelog:

v2.3.4 (2021-07-15)
-------------------
- Bump version: 2.3.3 → 2.3.4. [Petri Jokimies]


v2.3.3 (2021-07-15)
-------------------

Fix
~~~
- Add user agent to request for Yahoo quotes. [Petri Jokimies]







Other
~~~~~
- Bump version: 2.3.2 → 2.3.3. [Petri Jokimies]
- Change browsersync proxy back to localhost. [Petri Jokimies]
- New gitchangelog with new format. [Petri Jokimies]
- Update HISTORY. [Petri Jokimies]


v2.3.2 (2019-04-19)
-------------------
- Bump version: 2.3.1 → 2.3.2. [Petri Jokimies]
- Make iexcloud change percent decimal. [Petri Jokimies]







v2.3.1 (2019-04-12)
-------------------
- Bump version: 2.3.0 → 2.3.1. [Petri Jokimies]
- Fix IEXCloud change percentage. [Petri Jokimies]


v2.3.0 (2019-04-11)
-------------------
- Bump version: 2.2.2 → 2.3.0. [Petri Jokimies]
- Correct function to get possessions. [Petri Jokimies]



- Add possibility to fetch quote from IEXCloud. [Petri Jokimies]


v2.2.2 (2018-12-26)
-------------------
- Bump version: 2.2.1 → 2.2.2. [Petri Jokimies]
- Fix typo when calling Yahoo tracker. [Petri Jokimies]


v2.2.1 (2018-12-26)
-------------------
- Bump version: 2.2.0 → 2.2.1. [Petri Jokimies]
- Fix exhange name in Yahoo tracker. [Petri Jokimies]


v2.2.0 (2018-12-26)
-------------------
- Bump version: 2.1.6 → 2.2.0. [Petri Jokimies]
- Add Yahoo tracker. [Petri Jokimies]





v2.1.6 (2018-10-21)
-------------------
- Bump version: 2.1.5 → 2.1.6. [Petri Jokimies]
- Fix tests. [Petri Jokimies]
- Take AV tracker into account in tests. [Petri Jokimies]
- Mock out get_alpha_vantage_stock_quote. [Petri Jokimies]






- Fix Account.positions() renaming to get_positions. [Petri Jokimies]
- Rename Account.positions() to get_positions() [Petri Jokimies]










v2.1.5 (2018-10-19)
-------------------
- Bump version: 2.1.4 → 2.1.5. [Petri Jokimies]
- Ignore additinal files. [Petri Jokimies]
- Get currency from local backend. [Petri Jokimies]



- Define and use API wait time as constant. [Petri Jokimies]
- Add option to define API wait time on commandline. [Petri Jokimies]





v2.1.4 (2018-09-01)
-------------------

New
~~~
- Allow multiple updates to share prices. [Petri Jokimies]








- Add security listing. [Petri Jokimies]

Other
~~~~~
- Bump version: 2.1.3 → 2.1.4. [Petri Jokimies]
- Add optional delay when using AlphaVantage. [Petri Jokimies]



- Convert daily change to base currency. [Petri Jokimies]







v2.1.3 (2018-07-26)
-------------------
- Bump version: 2.1.2 → 2.1.3. [Petri Jokimies]
- Adjust AlphaVantage request rate. [Petri Jokimies]









- Cache AlphaVantage requests. [Petri Jokimies]















v2.1.2 (2018-07-12)
-------------------
- Bump version: 2.1.1 → 2.1.2. [Petri Jokimies]
- Add dayly change. [Petri Jokimies]


v2.1.1 (2018-06-10)
-------------------
- Bump version: 2.1.0 → 2.1.1. [Petri Jokimies]
- Use API key for fixer.io. [Petri Jokimies]





- Update history. [Petri Jokimies]


v2.1.0 (2018-06-03)
-------------------
- Bump version: 2.0.6 → 2.1.0. [Petri Jokimies]
- Use  AlphaVantatge as 'local' price provider. [Petri Jokimies]



- Add AlphaVantage as a price tracker. [Petri Jokimies]
- Fix(google): Remove debug logging. [Petri Jokimies]


v2.0.6 (2017-11-28)
-------------------
- Bump version: 2.0.5 → 2.0.6. [Petri Jokimies]
- Fix(google): Use local google finance proxy. [Petri Jokimies]
- Feat(quote api): Provide API for stock quotes. [Petri Jokimies]







- Test(google): Change Yahoo url in test. [Petri Jokimies]





v2.0.5 (2017-10-07)
-------------------
- Bump version: 2.0.4 → 2.0.5. [Petri Jokimies]
- Change google url. [Petri Jokimies]








v2.0.4 (2017-02-23)
-------------------
- Bump version: 2.0.3 → 2.0.4. [Petri Jokimies]
- Change Yahoo url. [Petri Jokimies]



- Docs(HISTORY): Update HISTORY. [Petri Jokimies]


v2.0.3 (2017-01-08)
-------------------
- Bump version: 2.0.2 → 2.0.3. [Petri Jokimies]
- Fix(): Don't load anglular-scripts in templates. [Petri Jokimies]








- Fix(summary): Fix improperly detected currency. [Petri Jokimies]









- Fix(): Use plain get in retrieving exchange rates. [Petri Jokimies]





- Docs(HISTORY): Update HISTORY. [Petri Jokimies]


v2.0.2 (2016-12-31)
-------------------
- Bump version: 2.0.1 → 2.0.2. [Petri Jokimies]
- Feat(bumpversion): Configure bumpversion. [Petri Jokimies]
- Test(): Add pytest & bumpversion to requirements. [Petri Jokimies]
- Fix(management): Set defaults to google quote. [Petri Jokimies]



- Fix(urls): Change deprecated django.conf.urls.patterns. [Petri
  Jokimies]
- Fix(DividendByYear): Fix JSON serialising. [Petri Jokimies]








- History update. [Petri Jokimies]


v2.0.1 (2016-12-10)
-------------------
- Bump version. [Petri Jokimies]
- Add migrations. [Petri Jokimies]



- Remove Python 3.3 from travis configuration. [Petri Jokimies]


v2.0.0 (2016-11-13)
-------------------
- Use Django 1.9.11. [Petri Jokimies]





v1.2.2 (2016-11-13)
-------------------
- Bump version. [Petri Jokimies]
- Update requirements for Python3. [Petri Jokimies]


v1.2.1 (2016-11-08)
-------------------
- Bump version to 1.2.1. [Petri Jokimies]
- Use newest version of django-currency-history. [Petri Jokimies]





v1.2.0 (2016-11-03)
-------------------
- Bump version 1.1.1 to 1.2.0. [Petri Jokimies]
- Add possibility to get quotes from Yahoo Finance. [Petri Jokimies]





- Fix(requirements): beatifulsoup added to requirements. [Petri
  Jokimies]


v1.1.1 (2016-03-06)
-------------------
- Feat(summary detail): Flash changed prices. [Petri Jokimies]



- Fix(account summary): Use latest date from Google Finance. [Petri
  Jokimies]



- Refactor(account summary): Sort table using Angular's orderBy. [Petri
  Jokimies]







- Test(securities service): Use smaller number of mocked results. [Petri
  Jokimies]



- Test(gulp): Output results in separate directory. [Petri Jokimies]



- Fix(account summary): $timeout parameters changed in 1.4.x. [Petri
  Jokimies]





- Test(account summary): More tests. [Petri Jokimies]
- Test(position service): Test for google_quote. [Petri Jokimies]
- Test(karma conf): Run coverage. [Petri Jokimies]


v1.1.0 (2016-02-16)
-------------------
- Test(): More files to watch in karma.conf. [Petri Jokimies]
- Test(): Added test for Angular currency service. [Petri Jokimies]
- Test(karma): Using jasmine-query for fixtures. [Petri Jokimies]
- Chore(gulp): First gulp tasks. [Petri Jokimies]
- Fix(account summary): Removed unnecessary DB queries. [Petri Jokimies]



- Feat(account summary): Use correct currency in calculations, use
  spinner. [Petri Jokimies]















- Feat(account summary): Added market value calculation. [Petri
  Jokimies]
- Feat(account summary): Display live values. [Petri Jokimies]
- Feat(account summary): Count total market value. [Petri Jokimies]
- Feat(account summary): Initial price live updates. [Petri Jokimies]



- Feat(): Added API to get list of holdings. [Petri Jokimies]
- Test(account): Make AccountBase more usable. [Petri Jokimies]





v1.0.1 (2016-01-15)
-------------------
- Fix(update prices): Adapt to KL's new web page. [Petri Jokimies]
- Fix(requirements): Specific about Django version. [Petri Jokimies]








v1.0.0 (2015-11-30)
-------------------
- Docs(): Added comments for management commads. [Petri Jokimies]
- Feat(): Add management commands to update prices. [Petri Jokimies]



- Refactor(test): Security test and factories separeted. [Petri
  Jokimies]
- Refactor(test): Price tests and factories sepateted. [Petri Jokimies]


v0.1.0 (2015-09-25)
-------------------
- Initial commit. [Petri Jokimies]







- Use mktval instead of value, everywhere. [Vinod Kurup]
- Typo value -> mktval. [Vinod Kurup]
- Revamps 'cash' property to be a dict of a 'cash' position. [Vinod
  Kurup]
- Test that basis is nonzero before dividing by it. [Vinod Kurup]
- Add test to make sure no DivByZero error if basis is zero. [Vinod
  Kurup]
- Implement stock splits. [Vinod Kurup]
- Revamped implementation. [Vinod Kurup]
- Pep8. [Vinod Kurup]
- Pep8 fixes. [Vinod Kurup]
- Remove trailing whitespace and div-by-zero. [Vinod Kurup]
- Remove fake file. [Vinod Kurup]
- Test2. [Vinod Kurup]
- Merge branch 'master' of github.com:/vkurup/stocks. [Vinod Kurup]
- Start a Price model. [Vinod Kurup]
- Make the text a little smaller. [Vinod Kurup]
- Receiving interest should not increase basis. [Vinod Kurup]
- Plan to add prices table. [Vinod Kurup]
- Add account-wide calculations. [Vinod Kurup]
- Fix negative account value problem. [Vinod Kurup]









- Another todo. [Vinod Kurup]
- Add date to positions function. [Vinod Kurup]
- Added some development notes. [Vinod Kurup]
- Test. [Vinod Kurup]
- Add Interest form and display. [Vinod Kurup]
- Start using Django Forms. [Vinod Kurup]
- Refactoring. [Vinod Kurup]
- Added total_return calcs and display. [Vinod Kurup]
- Calculate and display market value. [Vinod Kurup]
- Calculate and display cost basis. [Vinod Kurup]
- Planning for the changes I want to see. [Vinod Kurup]
- A little cleanup. [Vinod Kurup]
- Show active positions in a table. [Vinod Kurup]
- Initialize position with $CASH=0. [Vinod Kurup]
- Delete an account. [Vinod Kurup]
- Add FK relationship from Transaction to Account. [Vinod Kurup]
- Add 'buy security' link. [Vinod Kurup]
- Show 'Cash' on account page. [Vinod Kurup]
- Add calculated 'cash' property to Account. [Vinod Kurup]
- Add deposit view. [Vinod Kurup]





- Move account list to main URL. [Vinod Kurup]
- Added simple account creation. [Vinod Kurup]
- Fix code to pass tests. [Vinod Kurup]
- Next up: making value account for dividends. [Vinod Kurup]
- Start testing value functions. [Vinod Kurup]
- Beginnings of double entry in place. [Vinod Kurup]
- Refactored DIV and DEPOSIT to also use buy_transaction. [Vinod Kurup]
- Reuse buy_security for receive_interest. [Vinod Kurup]
- Using virtualenv means I don't need to specify python2. [Vinod Kurup]
- Added test to start working on double entry transactions. [Vinod
  Kurup]
- Few more tests. [Vinod Kurup]
- More TDD trials. [Vinod Kurup]
- First steps with TDD. [Vinod Kurup]
- Cool, don't need the 'portfolio' part there. [Vinod Kurup]
- Working on simple tests. [Vinod Kurup]
- Added ability to delete transactions. [Vinod Kurup]
- Refactored to use class based views. [Vinod Kurup]
- Move templates into app. [Vinod Kurup]
- Some initial SQL fixtures. [Vinod Kurup]
- Add an edit form. [Vinod Kurup]
- Added django-debug-toolbar. [Vinod Kurup]
- Missed one STATIC_URL. [Vinod Kurup]
- Just add some HTML5 boilerplate. [Vinod Kurup]
- Removed redundant template. [Vinod Kurup]
- Trying generic views. [Vinod Kurup]
- Beginnings of a data model. [Vinod Kurup]
- Let's use Django 1.4. [Vinod Kurup]
- Create first app. [Vinod Kurup]
- Make manage.py executable. [Vinod Kurup]
- Use sqlite3 for now. [Vinod Kurup]
- Initial README. [Vinod Kurup]
- Initial commit. [Vinod Kurup]


