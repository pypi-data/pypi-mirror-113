try:
    from .SekundeException import *
    from ....__VergleichsStamm import VergleichsStammZahl
except ImportError:
    from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
    from Kronos_heureka_code.Zeit.Uhrzeit.Sekunde.SekundeException import *


class Sekunde(VergleichsStammZahl):
    def __init__(self, sekunde: int):
        self.__sekunde: [int, None] = None
        self.sekunde = sekunde
        pass

    def __repr__(self):
        return f"<Sekunde {self.__str__()}>"

    def __str__(self):
        return str(self.sekunde).zfill(2) if self.sekunde else "00"

    def __int__(self):
        return self.sekunde

    @property
    def sekunde(self):
        return self.__sekunde

    @sekunde.setter
    def sekunde(self, sekunde: int):
        if sekunde is not None:
            if type(sekunde) != int:
                raise SekundeKeineGanzeZahl(sekunde)
            if sekunde < 0:
                raise SekundeZuKlein(sekunde)
            if sekunde > 60:
                raise SekundeZuGross(sekunde)
        self.__sekunde = sekunde
        pass
    pass
