# User-defined exceptions


class Error(Exception):
    """Base class for other exceptions"""
    pass


class Error400(Error):
    """Invalid ordering or Invalid filters or Wrong output fields or Invalid limits"""
    pass


class Error404(Error):
    """Not found"""
    pass


class ErrorUnknown(Error):
    """Error not defined"""
    pass
