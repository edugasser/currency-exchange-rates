class ExchangeProviderError(Exception):
    def __init__(self, error: str):
        self.error = error


class ExchangeCurrencyDoesNotExist(Exception):
    def __init__(self, error: str):
        self.error = error


class ExchangeCurrencyError(Exception):
    def __init__(self, error: str):
        self.error = error


class DecimalError(Exception):
    def __init__(self, error: str):
        self.error = error


class CurrencyDoesNotExist(Exception):
    def __init__(self, error: str):
        self.error = error
