"""Modul um die Zeitrechnung eines Jahres anzugeben"""


class Zeitrechnung:
    def __init__(self, name: str, kuerzel: str, delta: int):
        """Klasse zum verwalten einer Zeitrechnung

        @name: str: Der Name der Zeitrechnung

        @kuerzel: str: Die Abkuerzung der Zeitrechnung

        @delta: int: der Jahresunterschied zur Allgemeinen Zeitrechnung
        """
        # Der Name der Zeitrechnung
        self.__name: str = name
        # Die Abkuerzung der Zeitrechnung
        self.__kuerzel: str = kuerzel
        # Der Unterschied an Jahren von dieser zur Allgemeinen Zeitrechnung
        self.__delta: int = delta
        pass

    def __repr__(self):
        """Der Representations-String der Zeitrechnung

        :return str"""
        return f"<Zeitrechnung {self.kuerzel}>"

    def convert(self, jahr: int, ziel: "Zeitrechnung") -> int:
        """Konvertiert ein Jahr in eine andere Zeitrechnung:

        @jahr: int: das Jahr das konvertiert werden soll

        @zeitrechnung: Zeitrechnung: Die Zeitrechnung, zu der das Jahr konvertiert werden soll

        :raise TypeError: Wenn das Jahr keine ganze Zahl ist

        :return int
        """
        # TODO: Konvertierungsmethode pruefen
        if type(jahr) != int:
            try:
                jahr = int(jahr)
            except ValueError:
                raise TypeError("Das Jahr muss ein int sein")
        return jahr - self.delta + ziel.delta

    @property
    def delta(self) -> int:
        """Der Jahresunterschied zur Allgemeinen Zeitrechnung

        :return int"""
        return self.__delta

    @property
    def name(self) -> str:
        """Der Name der Zeitrechnung

        :return str"""
        return self.__name

    @property
    def kuerzel(self) -> str:
        """Das Kuerzel der Zeitrechnung

        :return str"""
        return self.__kuerzel

    pass


# TODO: A.u.c. Definition pruefen
# TODO: Weitere Zeitrechnungen hinzufuegen
A_U_C = Zeitrechnung("Ab urbem condita", "A.u.c.", 753)
A_Z = Zeitrechnung("Allgemeine Zeitrechnung", "A.Z.", 0)
