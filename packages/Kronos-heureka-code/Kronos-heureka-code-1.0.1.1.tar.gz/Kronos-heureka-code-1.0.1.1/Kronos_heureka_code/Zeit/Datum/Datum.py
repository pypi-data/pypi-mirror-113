from Kronos_heureka_code.Zeit.Datum.Monat import Monate, Monat
from Kronos_heureka_code.Zeit.Datum.Tag import Tag
from Kronos_heureka_code.Zeit.Datum.Jahr import Jahr
from Kronos_heureka_code.Zeit.Datum.Wochentag import Wochentag, Wochentage


class DatumsNotation:
    """Oberklasse fuer Datumsnotationen"""
    def convert(self, *args, **kwargs) -> "Datum":
        """Konvertiert eine Angabe eines Datums in einer gewissen Notation in ein Datum"""
        pass

    def __repr__(self):
        return f"<DatumsNotation {self.__class__.__name__}>"
    pass


class DatumsNotationNonSplitted(DatumsNotation):
    """Oberklasse fuer Datumsnotationen ohne Trennzeichen"""
    pass


class DatumsNotationSplitted(DatumsNotation):
    """Oberklasse fuer Datumsnotationen mit Trennzeichen"""
    def __init__(self, splitter: str = "."):
        self.__splitter: str = splitter
        pass

    @property
    def splitter(self) -> str:
        """Das Trennzeichen der Notation"""
        return self.__splitter
    pass


class TMJ(DatumsNotationSplitted):
    """Datumsnotation mit Trennzeichen der Folge Tag[Trenner]Monat[Trenner]Jahr

    Fuehrende Nullen werden dabei ignoriert

    z.B.:
    * 21/06/2000
    * 01.01.2001
    * 2-2-1900
    """
    def convert(self, s: str) -> "Datum":
        tag, monat, jahr = s.split(self.splitter)
        return Datum(tag=int(tag), monat=int(monat), jahr=int(jahr))
    pass


class JMT(DatumsNotationSplitted):
    """Datumsnotation mit Trennzeichen der Folge Jahr[Trenner]Monat[Trenner]Tag

    Fuehrende Nullen werden dabei ignoriert

    z.B.:

    * 2000/06/21
    * 2001.1.1
    * 1900-2-2
    """
    def convert(self, s: str) -> "Datum":
        jahr, monat, tag = s.split(self.splitter)
        return Datum(tag=int(tag), monat=int(monat), jahr=int(jahr))
    pass


class TTMMJJJJ(DatumsNotationNonSplitted):
    """Datumsnotation ohne Trennzeichen der Folge TagMonatJahr

    Das Jahr wird mit vier Ziffern angegeben

    Fuehrende Nullen muessen beachtet werden

    z.B.:

    * 21062000
    * 01012001
    * 02021900
    """
    def convert(self, s: str) -> "Datum":
        tag, monat, jahr = s[:2], s[2:4], s[4:8]
        return Datum(tag=int(tag), monat=int(monat), jahr=int(jahr))
    pass


class JJJJMMTT(DatumsNotationNonSplitted):
    """Datumsnotation ohne Trennzeichen der Folge JahrMonatTag

    Das Jahr wird hierbei mit vier Ziffern angegeben

    Fuehrende Nullen muessen beachtet werden

    z.B.:

    * 20000621
    * 20010101
    * 09000202
    """
    def convert(self, s: str) -> "Datum":
        jahr, monat, tag = s[:4], s[4:6], s[6:8]
        return Datum(tag=int(tag), monat=int(monat), jahr=int(jahr))
    pass


class Datum:
    def __init__(self, tag: int, monat: int, jahr: int):
        self.__tag: Tag = Tag(tag)
        self.__monat: Monat = Monate.get(monat).__copy__()
        self.__jahr: Jahr = Jahr(jahr)

        self.__tag.monats_pruefung(self.__monat, self.ist_schaltjahr(jahr))
        pass

    def __repr__(self):
        return f"<Datum {self.wochentag.wochentag_name}, " \
               f"{str(self.tag.tag).zfill(2)}.{str(self.monat.position.position).zfill(2)}.{self.jahr.jahr}>"

    @staticmethod
    def ist_schaltjahr(jahr: int):
        if jahr % 100 == 0:
            return jahr % 400 == 0
        return jahr % 4 == 0

    @property
    def wochentag(self) -> Wochentag:
        tagescode = self.tag.tag
        monatscode = self.monatscode
        jahrescode = self.jahrescode
        return Wochentage.get((tagescode + monatscode + jahrescode) % 7)

    @property
    def monatscode(self) -> int:
        monat = Monate.get(self.monat.position.position)
        code = monat.monatscode.monatscode
        if monat in [Monate.JANUAR, Monate.FEBRUAR] and Datum.ist_schaltjahr(int(self.jahr)):
            code -= 1
        return code

    @property
    def jahrescode(self) -> int:
        return {1: 5, 0: 0, 3: 1, 2: 3}[
                   (int(self.jahr) // 100) % 4] + (((int(self.__jahr) % 100) // 4) + int(self.__jahr) % 100) % 7

    @classmethod
    def von_datums_notation(cls, s, notation: DatumsNotation):
        return notation.convert(s)

    def __eq__(self, other: "Datum"):
        return self.jahr == other.jahr and self.monat == other.monat and self.tag == other.tag

    def __ne__(self, other: "Datum"):
        return self.__eq__(other) is False

    def __lt__(self, other: "Datum"):
        if self.jahr < other.jahr:
            return True
        if self.jahr > other.jahr:
            return False

        if self.monat < other.monat:
            return True
        if self.monat > other.monat:
            return False

        if self.tag < other.tag:
            return True
        if self.tag > other.tag:
            return False
        return False

    def __gt__(self, other: "Datum"):
        if self.jahr > other.jahr:
            return True
        if self.jahr < other.jahr:
            return False

        if self.monat > other.monat:
            return True
        if self.monat < other.monat:
            return False

        if self.tag > other.tag:
            return True
        if self.tag < other.tag:
            return False
        return False

    def __le__(self, other: "Datum"):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other: "Datum"):
        return self.__gt__(other) or self.__eq__(other)

    @property
    def tag(self) -> Tag:
        return self.__tag

    @property
    def monat(self) -> Monat:
        return self.__monat

    @property
    def jahr(self):
        return self.__jahr
    pass


# Tag[T/TT].Monat[M/MM].Jahr[JJ/JJJJ] z.B. 21.06.2000
TMJ_DOT = TMJ(".")
# Tag[T/TT]-Monat[M/MM]-Jahr[JJ/JJJJ] z.B. 21-06-2000
TMJ_DASH = TMJ("-")
# Tag[T/TT]/Monat[M/MM]/Jahr[JJ/JJJJ] z.B. 21/06/2000
TMJ_SLASH = TMJ("/")

# Jahr[JJ/JJJJ].Monat[M/MM].Tag[T/TT] z.B. 2000.06.21
JMT_DOT = JMT(".")
# Jahr[JJ/JJJJ]-Monat[M/MM]-Tag[T/TT] z.B. 2000-06-21
JMT_DASH = JMT("-")
# Jahr[JJ/JJJJ]/Monat[M/MM]/Tag[T/TT] z.B. 2000/06/21
JMT_SLASH = JMT("/")

# Tag[TT]Monat[MM]Jahr[JJJJ] z.B. 21062000
TTMMJJJJ_NON_SPLITTED = TTMMJJJJ()
# Jahr[JJJJ]Monat[MM]Tag[TT] z.B. 20000621
JJJJMMTT_NON_SPLITTED = JJJJMMTT()
