try:
    from ..DatumException import DatumException
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.DatumException import DatumException


class WochentagException(DatumException):
    pass


class UngueltigerWochentagname(WochentagException):
    pass


class UngueltigeWochentagposition(WochentagException):
    pass
