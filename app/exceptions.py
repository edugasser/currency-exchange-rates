class ExchangeProviderError(Exception):
    def __init__(self, error: str):
        self.error = error


class ExchangeCurrencyDoesNotExist(Exception):
    def __init__(self, error: str):
        self.error = error
