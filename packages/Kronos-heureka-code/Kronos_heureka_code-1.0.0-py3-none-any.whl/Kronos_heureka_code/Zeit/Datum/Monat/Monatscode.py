try:
    from .MonatsException import KeinGueltigerMonatscode
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Monat.MonatsException import KeinGueltigerMonatscode


class Monatscode:
    def __init__(self, monatscode: [int, "Monatscode"]):
        self.__monatscode: [int, None] = None
        self.monatscode = monatscode
        pass

    @property
    def monatscode(self) -> int:
        return self.__monatscode

    @monatscode.setter
    def monatscode(self, monatscode: int):
        if type(monatscode) == float:
            raise KeinGueltigerMonatscode(f"{monatscode} ist kein gueltiger Monatscode")
        try:
            monatscode = int(monatscode)
        except ValueError:
            raise KeinGueltigerMonatscode(f"Der Monatscode {monatscode} ist ungueltig")

        self.__monatscode = monatscode

    def __int__(self):
        return self.monatscode

    def __repr__(self):
        return f"<Monatscode {self.monatscode}>"
    pass
