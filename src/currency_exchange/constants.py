class TypeProvider(object):
    FIXER_IO = 'FIXER'
    MOCK = 'MOCK'

    choices = (
        (FIXER_IO, "Fixer IO"),
        (MOCK, "Mock")
    )


class DecimalPrecission(object):
    DECIMAL_PLACES = 6
    MAX_DIGITS = 18
