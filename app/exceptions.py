class ExchangeProviderError(Exception):
    def __init__(self, error: str):
        self.error = error
