try:
    from ..UhrzeitException import UhrzeitException
except ImportError:
    from Kronos_heureka_code.Zeit.Uhrzeit.UhrzeitException import UhrzeitException


class MinuteException(UhrzeitException):
    pass


class MinuteKeineGanzeZahl(MinuteException):
    def __init__(self, minute):
        super(MinuteKeineGanzeZahl, self).__init__(f"{minute} Minute muss eine ganze Zahl sein (int)")
    pass


class MinuteZuGross(MinuteException):
    def __init__(self, minute):
        super(MinuteZuGross, self).__init__(f"Eine Minute darf maximal 59 sein. Nicht {minute}")
    pass


class MinuteZuKlein(MinuteException):
    def __init__(self, minute):
        super(MinuteZuKlein, self).__init__(f"{minute} muss zwischen 0 und exklusive 60 liegen")
    pass
