try:
    from ..UhrzeitException import UhrzeitException
except ImportError:
    from Kronos_heureka_code.Zeit.Uhrzeit.UhrzeitException import UhrzeitException


class SekundeException(UhrzeitException):
    pass


class SekundeKeineGanzeZahl(SekundeException):
    def __init__(self, sekunde):
        super(SekundeKeineGanzeZahl, self).__init__(f"{sekunde} muss eine ganze Zahl sein (int)")
    pass


class SekundeZuGross(SekundeException):
    def __init__(self, sekunde):
        super(SekundeZuGross, self).__init__(f"Eine Sekunde darf maximal 59 sein. Nicht {sekunde}")
    pass


class SekundeZuKlein(SekundeException):
    def __init__(self, sekunde):
        super(SekundeZuKlein, self).__init__(f"{sekunde} muss zwischen 0 und exklusive 60 liegen")
    pass
