try:
    from .MonatsException import KeineGueltigeMonatsposition
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Monat.MonatsException import KeineGueltigeMonatsposition


class Monatsposition:
    def __init__(self, position: [int, "Monatsposition"]):
        self.__position: [int, None] = None
        self.position = position
        pass

    @property
    def position(self) -> int:
        return self.__position

    @position.setter
    def position(self, position: int):
        try:
            position = int(position)
        except ValueError:
            raise KeineGueltigeMonatsposition(f"Der Monat \"{position}\" ist keine gueltige Zahl")

        if position < 1 or position > 12:
            raise KeineGueltigeMonatsposition(f"Eine Monatsposition muss zwischen 1 und 12 liegen, nicht {position}")

        self.__position = position
        pass

    def __int__(self):
        return self.position

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.position}>"

    pass
