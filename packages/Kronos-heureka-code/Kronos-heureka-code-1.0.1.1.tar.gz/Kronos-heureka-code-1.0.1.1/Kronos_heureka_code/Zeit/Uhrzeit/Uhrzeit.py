from Kronos_heureka_code.Zeit.Uhrzeit.UhrzeitException import *
from Kronos_heureka_code.Zeit.Uhrzeit.Minute import Minute
from Kronos_heureka_code.Zeit.Uhrzeit.Stunde import Stunde
from Kronos_heureka_code.Zeit.Uhrzeit.Sekunde import Sekunde

from Kronos_heureka_code.Zeit.Uhrzeit.Minute.MinuteException import *
from Kronos_heureka_code.Zeit.Uhrzeit.Stunde.StundeException import *
from Kronos_heureka_code.Zeit.Uhrzeit.Sekunde.SekundeException import *


class UhrzeitNotation:
    """Oberklasse fuer Uhrzeitnotationen"""
    def convert(self, *args, **kwargs) -> "Uhrzeit":
        """Konvertiert eine Angabe einer Uhrzeit in einer gewissen Notation in eine Uhrzeit"""
        pass

    def __repr__(self):
        return f"<UhrzeitNotation {self.__class__.__name__}>"
    pass


class UhrzeitNotationNonSplitted(UhrzeitNotation):
    """Oberklasse fuer Uhrzeitnotationen ohne Trennzeichen"""
    pass


class UhrzeitNotationSplitted(UhrzeitNotation):
    """Oberklasse fuer Uhrzeitnotationen mit Trennzeichen"""
    def __init__(self, splitter: str = "."):
        self.__splitter: str = splitter
        pass

    @property
    def splitter(self) -> str:
        """Das Trennzeichen der Notation"""
        return self.__splitter
    pass


class HMS(UhrzeitNotationSplitted):
    def convert(self, s: str) -> "Uhrzeit":
        splitted = s.split(self.splitter)
        if len(splitted) == 2:
            return Uhrzeit(stunde=int(splitted[0]), minute=int(splitted[1]))
        elif len(splitted) == 3:
            return Uhrzeit(stunde=int(splitted[0]), minute=int(splitted[1]), sekunde=int(splitted[2]))
        else:
            raise UhrzeitException(f"{s} enthaelt fuer diese Notation zu wenige Werte")
    pass


class SMH(UhrzeitNotationSplitted):
    def convert(self, s: str) -> "Uhrzeit":
        splitted = s.split(self.splitter)
        if len(splitted) == 2:
            return Uhrzeit(stunde=int(splitted[0]), minute=int(splitted[1]))
        elif len(splitted) == 3:
            return Uhrzeit(stunde=int(splitted[0]), minute=int(splitted[1]), sekunde=int(splitted[2]))
        else:
            raise UhrzeitException(f"{s} enthaelt fuer diese Notation zu wenige Werte")
    pass


class HHMMSS(UhrzeitNotationNonSplitted):
    def convert(self, s: str) -> "Uhrzeit":
        stunde, minute, sekunde = s[0:2], s[2:4], s[4:6]
        if sekunde != "":
            return Uhrzeit(stunde=int(stunde), minute=int(minute), sekunde=int(sekunde))
        return Uhrzeit(stunde=int(stunde), minute=int(minute))


class SSMMHH(UhrzeitNotationNonSplitted):
    def convert(self, s: str) -> "Uhrzeit":
        sekunde, minute, stunde = s[0:2], s[2:4], s[4:6]
        if sekunde != "":
            return Uhrzeit(stunde=int(stunde), minute=int(minute), sekunde=int(sekunde))
        return Uhrzeit(stunde=int(stunde), minute=int(minute))


class Uhrzeit:
    def __init__(self, stunde: int, minute: int, sekunde: int = None):
        self.__stunde:   Stunde = Stunde(stunde)
        self.__minute:   Minute = Minute(minute)
        self.__sekunde: Sekunde = Sekunde(sekunde)
        pass

    def __repr__(self):
        return f"<Uhrzeit {self.__stunde.__str__()}:{self.__minute.__str__()}:{self.__sekunde.__str__()}>"

    @classmethod
    def von_uhrzeit_notation(cls, s, notation: UhrzeitNotation):
        return notation.convert(s)

    def __eq__(self, other: "Uhrzeit"):
        return self.stunde == other.stunde and self.minute == other.minute and self.sekunde == other.sekunde

    def __ne__(self, other: "Uhrzeit"):
        return self.__eq__(other) is False

    def __lt__(self, other: "Uhrzeit"):
        if self.stunde < other.stunde:
            return True
        if self.stunde > other.stunde:
            return False
        if self.minute < other.minute:
            return True
        if self.minute > other.minute:
            return False
        if self.sekunde < other.sekunde:
            return True
        return False

    def __gt__(self, other: "Uhrzeit"):
        if self.stunde > other.stunde:
            return True
        if self.stunde < other.stunde:
            return False
        if self.minute > other.minute:
            return True
        if self.minute < other.minute:
            return False
        if self.sekunde > other.sekunde:
            return True
        return False

    def __le__(self, other: "Uhrzeit"):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other: "Uhrzeit"):
        return self.__gt__(other) or self.__eq__(other)

    @property
    def stunde(self):
        return self.__stunde

    @property
    def minute(self):
        return self.__minute

    @property
    def sekunde(self):
        return self.__sekunde
    pass


# Stunde[H/HH].Minute[M/MM].Sekunde[S/SS] z.B. 09.00.05
HMS_DOT = HMS(".")
# Stunde[H/HH]:Minute[M/MM]:Sekunde[S/SS] z.B. 09:00:05
HMS_COLON = HMS(":")
# Stunde[H/HH]-Minute[M/MM]-Sekunde[S/SS] z.B. 09-00-05
HMS_DASH = HMS("-")
# Stunde[H/HH]/Minute[M/MM]/Sekunde[S/SS] z.B. 09/00/05
HMS_SLASH = HMS("/")

# Sekunde[S/SS].Minute[M/MM].Stunde[H/HH] z.B. 05.00.09
SMH_DOT = SMH(".")
# Sekunde[S/SS]:Minute[M/MM]:Stunde[H/HH] z.B. 09:00:05
SMH_COLON = SMH(":")
# Sekunde[S/SS]-Minute[M/MM]-Stunde[H/HH] z.B. 05-00-09
SMH_DASH = SMH("-")
# Sekunde[S/SS]/Minute[M/MM]/Stunde[H/HH] z.B. 05/00/09
SMH_SLASH = SMH("/")

# Stunde[HH]Minute[MM]Sekunde[SS] z.B. 090005
HHMMSS_NON_SPLITTED = HHMMSS()
# Sekunde[SS]Minute[MM]Stunde[HH] z.B. 050009
SSMMHH_NON_SPLITTED = SSMMHH()
