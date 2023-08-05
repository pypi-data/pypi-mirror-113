from Kronos_heureka_code.__VergleichsStamm import VergleichsStammZahl
from Kronos_heureka_code.Zeit.Datum.Jahr.JahrException import *
from Kronos_heureka_code.Zeit.Datum.Jahr.Zeitrechnung import *


class Jahr(VergleichsStammZahl):
    def __init__(self, jahr: int, zeitrechnung: Zeitrechnung = A_Z):
        """Klasse zum verwalten einer Jahreszahl einer Zeitrechnung

        @jahr: int: Das Jahr, das gespeichert werden soll

        @zeitrechnung: Zeitrechnung: Die Zeitrechnung des Jahres, Standard ist die Allgemeine Zeitrechnung

        :raises TypeError: Wird geworfen, wenn keine Zeitrechnung gegeben wurde
        :raises JahrKeineGanzeZahl: Wird geworfen, wenn das Jahr keine ganze Zahl ist
        """
        self.__jahr: [int, None] = None
        self.__zeitrechnung: Zeitrechnung = zeitrechnung
        self.jahr = jahr
        self.zeitrechnung = zeitrechnung
        pass

    def __int__(self):
        """Das Jahr als Zahl"""
        return self.jahr

    def __repr__(self):
        """Ein Representations-String fuer das Objekt"""
        return f"<Jahr {self.jahr} {self.zeitrechnung.kuerzel}>"

    @property
    def zeitrechnung(self):
        """Die Zeitrechnung des Jahres"""
        return self.__zeitrechnung

    @zeitrechnung.setter
    def zeitrechnung(self, z: Zeitrechnung):
        """Die Zeitrechnung setzen"""
        if type(z) != Zeitrechnung:
            raise TypeError("Keine Zeitrechnung angegeben")
        self.jahr = self.zeitrechnung.convert(self.jahr, z)
        self.__zeitrechnung = z
        pass

    @property
    def jahr(self) -> int:
        """Das Jahr als Zahl"""
        return self.__jahr

    @jahr.setter
    def jahr(self, jahr: int):
        """Das Jahr setzen"""
        exception_geworfen = False
        try:
            # Das Argument konvertieren
            self.__jahr: int = int(jahr)
        except ValueError:
            exception_geworfen = True
        except TypeError:
            exception_geworfen = True
        # Falls das Argument nicht konvertiert werden konnte
        if exception_geworfen:
            raise JahrKeineGanzeZahl(f"Das Attribut \"{jahr}\" ist kein gueltiges Jahr, "
                                     f"da es keine (ganze) Zahl ist oder nicht konvertiert werden kann.")
        self.__jahr = jahr
        pass
    pass
