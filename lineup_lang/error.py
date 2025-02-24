class LineupError(Exception):
    """Base class for exceptions in this module."""
    pass


class ExecutorFunctionAlreadyExistError(LineupError):
    """Two core object define the same function"""
    pass


class FunctionNotExistError(LineupError):
    """Function not exist in a language object"""
    pass


class ExecutorFunctionNotExistError(FunctionNotExistError):
    """Function not exist in a language executor"""
    pass


class ArgumentNotExistError(LineupError):
    """The script need an argument that is not present"""
    pass


class DecodeLineStringError(LineupError):
    """An error occur when decoding a line"""
    pass
