try:
    from .MonatsException import KeineGueltigeTageszahl
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Monat.MonatsException import KeineGueltigeTageszahl


class AnzahlTageImMonat:
    def __init__(self, anzahl_tage: int):
        self.__anzahl_tage: int = anzahl_tage
        pass

    @property
    def anzahl_tage(self) -> int:
        return self.__anzahl_tage

    @anzahl_tage.setter
    def anzahl_tage(self, anzahl_tage: int):
        try:
            anzahl_tage = int(anzahl_tage)
        except ValueError:
            raise KeineGueltigeTageszahl(f"{anzahl_tage} ist keine gueltige anzahl Tage fuer einen Monat")
        pass

    def __int__(self):
        return self.anzahl_tage

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.anzahl_tage}>"

    def __str__(self):
        return str(self.anzahl_tage)

    def __eq__(self, other: "AnzahlTageImMonat"):
        return self.anzahl_tage == other.anzahl_tage

    def __ne__(self, other):
        return self.__eq__(other) is False

    pass
