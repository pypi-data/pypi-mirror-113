try:
    from .WochentagException import *
    from .WochentagName import *
    from .WochentagPosition import *
    from ....__VergleichsStamm import VergleichsStammZahl
except ImportError:
    from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
    from Kronos_heureka_code.Zeit.Datum.Wochentag.WochentagException import *
    from Kronos_heureka_code.Zeit.Datum.Wochentag.WochentagName import *
    from Kronos_heureka_code.Zeit.Datum.Wochentag.WochentagPosition import *


class Wochentag(VergleichsStammZahl):
    def __init__(self, name: str, position: int):
        self.__wochentag_name:      WochentagName = WochentagName(name)
        self.__wochentag_position:  WochentagPosition = WochentagPosition(position)
        pass

    @property
    def wochentag_name(self):
        return self.__wochentag_name

    @property
    def wochentag_position(self):
        return self.__wochentag_position

    def __repr__(self):
        return f"<Wochentag {self.wochentag_name.wochentag_name} {self.wochentag_position.wochentag_position}>"

    def __int__(self):
        return int(self.wochentag_position)
    pass


class Wochentage:
    class WochentageIterator:
        def __init__(self):
            self.__position: int = 0
            pass

        @property
        def position(self) -> int:
            return self.__position

        def __next__(self):
            self.__position += 1
            return Wochentage.get(self.position - 1)

    SONNTAG:    Wochentag = Wochentag("Sonntag",    0)
    MONTAG:     Wochentag = Wochentag("Montag",     1)
    DIENSTAG:   Wochentag = Wochentag("Dienstag",   2)
    MITTWOCH:   Wochentag = Wochentag("Mittwoch",   3)
    DONNERSTAG: Wochentag = Wochentag("Donnerstag", 4)
    FREITAG:    Wochentag = Wochentag("Freitag",    5)
    SAMSTAG:    Wochentag = Wochentag("Samstag",    6)

    @staticmethod
    def get(item) -> Wochentag:
        return [Wochentage.SONNTAG, Wochentage.MONTAG, Wochentage.DIENSTAG,
                Wochentage.MITTWOCH, Wochentage.DONNERSTAG, Wochentage.FREITAG, Wochentage.SAMSTAG][item]

    def __getitem__(self, item) -> Wochentag:
        return self.get(item)

    def __iter__(self):
        return self.WochentageIterator()
