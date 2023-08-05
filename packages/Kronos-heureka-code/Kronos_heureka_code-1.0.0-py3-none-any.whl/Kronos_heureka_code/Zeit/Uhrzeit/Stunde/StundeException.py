from Kronos_heureka_code.Zeit.Uhrzeit.UhrzeitException import UhrzeitException


class StundeException(UhrzeitException):
    pass


class StundeKeineGanzeZahl(StundeException):
    def __init__(self, stunde):
        super(StundeKeineGanzeZahl, self).__init__(f"{stunde} Stunde muss eine ganze Zahl sein (int)")
    pass


class StundeZuGross(StundeException):
    def __init__(self, stunde):
        super(StundeZuGross, self).__init__(f"Eine Stunde darf maximal 23 sein. Nicht {stunde}")
    pass


class StundeZuKlein(StundeException):
    def __init__(self, stunde):
        super(StundeZuKlein, self).__init__(f"{stunde} muss zwischen 0 und exklusive 24 liegen")
    pass
