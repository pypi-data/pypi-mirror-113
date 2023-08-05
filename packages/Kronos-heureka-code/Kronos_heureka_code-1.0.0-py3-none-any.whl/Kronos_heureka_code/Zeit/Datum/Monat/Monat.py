try:
    from .MonatsException import *
    from .AnzahlTageImMonat import *
    from .Monatscode import *
    from .Monatsposition import *
    from .Monatsname import *
    from Kronos_heureka_code.__VergleichsStamm import *
except ImportError:
    from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
    from Kronos_heureka_code.Zeit.Datum.Monat.MonatsException import *
    from Kronos_heureka_code.Zeit.Datum.Monat.AnzahlTageImMonat import *
    from Kronos_heureka_code.Zeit.Datum.Monat.Monatscode import *
    from Kronos_heureka_code.Zeit.Datum.Monat.Monatsposition import *
    from Kronos_heureka_code.Zeit.Datum.Monat.Monatsname import *


class Monat(VergleichsStammZahl):
    """Speichert einen Monat mit:

    @name, dem Namen des Monats (In einem "Monatsname"-Objekt gespeichert)

    @position, der Positon des Monats in der Reihenfolge des Jahres (In einem "Monatsposition"-Objekt gespeichert)

    @monatscode, der Code zur Errechnung des Wochentags (In einem "Monatscode"-Objekt gespeichert)

    @anzahl_tage, die Anzahl Tage, die der Monat in einem nicht Schaltjahr hat (In einem "AnzahlTageImMonat"-Objekt gespeichert)

    @anzahl_tage_schaltjahr, die Anzahl Tage, die der Monat in einem Schaltjahr hat. Per default entspricht dies "anzahl_tage" (In einem "AnzahlTageImMonat"-Objekt gespeichert)"""
    def __init__(self, name: str, position: int, monatscode: int, anzahl_tage: int, anzahl_tage_schaltjahr: int = None):
        self.__name: Monatsname = Monatsname(name)
        self.__monats_position: Monatsposition = Monatsposition(position)
        self.__monatscode: Monatscode = Monatscode(monatscode)
        self.__anzahl_tage: AnzahlTageImMonat = AnzahlTageImMonat(anzahl_tage)
        self.__anzahl_tage_schaltjahr: AnzahlTageImMonat = AnzahlTageImMonat(
            anzahl_tage_schaltjahr if anzahl_tage_schaltjahr else anzahl_tage)

        pass

    def __copy__(self):
        return Monat(self.name.monatsname, self.position.position, self.monatscode.monatscode,
                     self.anzahl_tage.anzahl_tage, self.anzahl_tage_im_schaltjahr.anzahl_tage)

    def __repr__(self):
        s = f" anzahl_tage_schaltjahr={self.anzahl_tage_im_schaltjahr.anzahl_tage}>" \
            if (self.anzahl_tage != self.anzahl_tage_im_schaltjahr) else ">"
        return f"<Monat name={self.name} position={self.position.position} monatscode={self.monatscode.monatscode} " \
               f"anzahl_tage={self.anzahl_tage.anzahl_tage}" + s

    def __str__(self):
        return self.name.monatsname

    def __int__(self):
        return int(self.position)

    @property
    def name(self) -> Monatsname:
        """Der Name des jeweiligen Monats"""
        return self.__name

    @property
    def position(self) -> Monatsposition:
        """Die Position des Monats im Jahr (Bei 1 beginnend)"""
        return self.__monats_position

    @property
    def monatscode(self) -> Monatscode:
        """Der fuer die Wochentagsberechnung erforderliche Monatscode"""
        return self.__monatscode

    @property
    def anzahl_tage(self) -> AnzahlTageImMonat:
        """Die Anzahl Tage im Monat in einem nicht Schaltjahr"""
        return self.__anzahl_tage

    @property
    def anzahl_tage_im_schaltjahr(self) -> AnzahlTageImMonat:
        """Die Anzahl Tage im Monat in einem Schaltjahr"""
        return self.__anzahl_tage_schaltjahr

    pass


class Monate:
    """Enthaelt die verschiedenen Monate des Jahres:

    JANUAR, FEBRUAR, MAERZ, APRIL, MAI, JUNI, JULI, AUGUST, SEPTEMBER, OKTOBER, NOVEMBER, DEZEMBER


    Als Konstanten verfügbar: z.B. Monate.JANUAR, Monate.FEBRUAR


    Oder mit einem Index ueber die statische Methode get erhaltbar:
    z.B. Monate.get(1) = Monate.JANUAR; Monate.get(12) = Monate.DEZEMBER"""
    JANUAR:         Monat = Monat("Januar",     1,  6, 31)
    FEBRUAR:        Monat = Monat("Februar",    2,  2, 28, 29)
    MAERZ:          Monat = Monat("Maerz",      3,  2, 31)
    APRIL:          Monat = Monat("April",      4,  5, 30)
    MAI:            Monat = Monat("Mai",        5,  0, 31)
    JUNI:           Monat = Monat("Juni",       6,  3, 30)
    JULI:           Monat = Monat("Juli",       7,  5, 31)
    AUGUST:         Monat = Monat("August",     8,  1, 31)
    SEPTEMBER:      Monat = Monat("September",  9,  4, 30)
    OKTOBER:        Monat = Monat("Oktober",    10, 6, 31)
    NOVEMBER:       Monat = Monat("November",   11, 2, 30)
    DEZEMBER:       Monat = Monat("Dezember",   12, 4, 31)

    @staticmethod
    def get(item) -> Monat:
        return [Monate.JANUAR, Monate.FEBRUAR, Monate.MAERZ, Monate.APRIL, Monate.MAI, Monate.JUNI, Monate.JULI,
                Monate.AUGUST, Monate.SEPTEMBER, Monate.OKTOBER, Monate.NOVEMBER, Monate.DEZEMBER][item -1]

    pass
