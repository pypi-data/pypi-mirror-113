try:
    from ..DatumException import DatumException
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.DatumException import DatumException


class MonatsException(DatumException):
    pass


class KeineGueltigeMonatsposition(MonatsException):
    pass


class KeinGueltigerMonatscode(MonatsException):
    pass


class KeineGueltigeTageszahl(MonatsException):
    pass


class KeinGueltigerMonatsname(MonatsException):
    pass
