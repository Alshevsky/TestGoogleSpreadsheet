class ValuteException(Exception):
    message = 'Данные не содержат курс'

    def __init__(self):
        super().__init__(self.message)


class OutDatedException(Exception):
    message = 'Курс устарел'

    def __init__(self):
        super().__init__(self.message)
