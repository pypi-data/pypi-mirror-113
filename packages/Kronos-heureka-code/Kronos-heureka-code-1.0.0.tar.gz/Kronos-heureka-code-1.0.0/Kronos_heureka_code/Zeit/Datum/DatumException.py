try:
    from ..ZeitException import ZeitException
except ImportError:
    from Kronos_heureka_code.Zeit.ZeitException import ZeitException


class DatumException(ZeitException):
    pass
