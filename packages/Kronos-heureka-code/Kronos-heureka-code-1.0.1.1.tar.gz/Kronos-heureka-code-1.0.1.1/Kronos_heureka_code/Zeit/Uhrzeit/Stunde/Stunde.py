from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
from Kronos_heureka_code.Zeit.Uhrzeit.Stunde.StundeException import *


class Stunde(VergleichsStammZahl):
    def __init__(self, stunde: int):
        self.__stunde: [int, None] = None
        self.stunde = stunde
        pass

    def __repr__(self):
        return f"<Stunde {self.__str__()}>"

    def __str__(self):
        return str(self.stunde).zfill(2) if self.stunde else "00"

    def __int__(self):
        return self.stunde

    @property
    def stunde(self):
        return self.__stunde

    @stunde.setter
    def stunde(self, stunde: int):
        if type(stunde) != int:
            raise StundeKeineGanzeZahl(stunde)
        if stunde < 0:
            raise StundeZuKlein(stunde)
        if stunde > 60:
            raise StundeZuGross(stunde)
        self.__stunde = stunde
        pass
    pass
