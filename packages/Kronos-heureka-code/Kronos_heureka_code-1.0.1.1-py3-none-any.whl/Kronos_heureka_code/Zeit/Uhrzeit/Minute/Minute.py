try:
    from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
    from Kronos_heureka_code.Zeit.Uhrzeit.Minute.MinuteException import *
except ModuleNotFoundError:
    from .MinuteException import *
    from ....__VergleichsStamm import VergleichsStammZahl


class Minute(VergleichsStammZahl):
    def __init__(self, minute: int):
        self.__minute: [int, None] = None
        self.minute = minute
        pass

    def __repr__(self):
        return f"<Minute {self.__str__()}>"

    def __str__(self):
        return str(self.minute).zfill(2) if self.minute else "00"

    def __int__(self):
        return self.minute

    @property
    def minute(self):
        return self.__minute

    @minute.setter
    def minute(self, minute: int):
        if type(minute) != int:
            raise MinuteKeineGanzeZahl(minute)
        if minute < 0:
            raise MinuteZuKlein(minute)
        if minute > 60:
            raise MinuteZuGross(minute)
        self.__minute = minute
        pass
    pass
