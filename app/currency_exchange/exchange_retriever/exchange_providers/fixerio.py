from typing import List
from dateutil import parser
import requests

from app.app.settings import API_KEY_FIXER
from app.currency_exchange.exchange_retriever.exchange_response import \
    ExchangeResponse, CurrencyRate
from app.currency_exchange.exchange_retriever.exchange_retriever import ExchangeProvider
from app.exceptions import ExchangeProviderError


class FixerProvider(ExchangeProvider):
    endpoint = "http://data.fixer.io/api/{path}"

    def make_request(self, path, params):
        data = {"access_key": API_KEY_FIXER}
        data.update(params)
        try:
            response = requests.get(
                self.endpoint.format(path),
                params=data
            ).json()
        except Exception as e:
            raise ExchangeProviderError(
                f"Error trying to get data from Fixer io: {e}"
            )
        return response

    @staticmethod
    def transform_response(response):
        rates = []
        for currency, ratio in response["rates"].items():
            rates.append(CurrencyRate(currency, ratio))

        return ExchangeResponse(
            response["success"],
            parser.parse(response["date"]),
            response["base"],
            rates
        )

    def get_latest(self, currencies: List[str]) -> ExchangeResponse:
        response = self.make_request("latest", ",".join(currencies))
        return self.transform_response(response)

    def get_historical(self, exchange_date) -> ExchangeResponse:
        response = self.make_request(exchange_date.strftime("%Y-%m-%d"))
        return self.transform_response(response)
