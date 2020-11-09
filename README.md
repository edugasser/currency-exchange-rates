# Currency Exchange Rates API
>Web platform that allows users to calculate currency exchange rates.

Use the provider Fixer.io to retrieve and store daily currency
rates. It has to be designed to use multiple
currency data providers. So, it won’t only work with Fixer.io but also with any
other providers that might have different APIs for retrieving currency exchange
rates.

![Alt text](dashboard_screenshot?raw=true "Dashboard")
![Alt text](doc_screenshot?raw=true "Dashboard")

# Use cases
  - Retrieve and store daily currency rates. ([update daily rates])
  - List currency rates for a specific time period.([retrieve rates])
  - Calculate amount in a currency exchanged into a different currency.([calculate currency])
  - Retrieve time-weighted rate of return for any given amount invested from a currency into another one from given date until today.([calculate twr])
  - Import currency exchange rates from csv file.([import csv])
# Versioning
The API could manage different versions.
# Installation

Requires [Docker Compose](https://docs.docker.com/compose/install/) and [Docker](https://docs.docker.com/engine/install/ubuntu/) to run.

```sh
$ docker-compose up
```

## API Documentation
Swagger API documentation
- http://127.0.0.1:8000/docs/

## Usage
The app will setup initial data: 
> Currency Exchange Rates from 1 year for the different currencies: EUR, USD, GBP, CHF (https://excelrates.com)
> Admin user: admin/123456789A
- See the dasboard: http://localhost:8000
- See the admin: http://localhost:8000/admin (admin/123456789A)
- API List currency: http://127.0.0.1:8000/api/v1/historical/EUR/2020-01-01/2020-02-01/
- API Convert currency: http://127.0.0.1:8000/api/v1/convert/EUR/USD/?amount=10
- API Retrieve TWR: http://127.0.0.1:8000/api/v1/twr/EUR/USD/2020-01-01/?amount=10
- Daily currency exchange rates: `python manage.py update_currency_exchanges`
- Import CSV: `ImportCurrencyExchangeRates(repository).execute(file_name)`

## Tech
Uses a number of open source projects to work properly:

* [Django 2.2.17](https://www.djangoproject.com/) - Django
* [Django Rest Framework 3.12.2](https://www.django-rest-framework.org) - Django Rest Framework
* [PostgreSQl](https://www.postgresql.org/) - PostgreSQl
* [Python 3.8](https://www.python.org/downloads/release/python-380/) - Python 3.8

### Development
```sh
$ docker exec -it django sh
$ cd src
```
#### Tests
```sh
$ python manage.py test 
```
#### Coverage
```sh
$ coverage run --source='.' manage.py test
$ coverage report
TOTAL                                                                               776     67    91%
```
#### Lint
```sh
$ python -m flake8
```
[StartAdmin](https://www.bootstrapdash.com/product/star-admin-free/)

[import csv]: <https://github.com/edugasser/currency-exchange-rates/blob/master/src/currency_exchange/use_cases/import_currency_exchange_rates.py>
 [update daily rates]: <https://github.com/edugasser/currency-exchange-rates/blob/master/src/currency_exchange/use_cases/update_currency_exchange_rate.pyy>
 [calculate currency]: <https://github.com/edugasser/currency-exchange-rates/blob/master/src/currency_exchange/use_cases/convert_currency.py>
 [retrieve rates]: <https://github.com/edugasser/currency-exchange-rates/blob/master/src/currency_exchange/use_cases/retrieve_currency_exchange_rate.py>
 [calculate twr]: <https://github.com/edugasser/currency-exchange-rates/blob/master/src/currency_exchange/use_cases/retrieve_twr.py>
