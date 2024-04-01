class LineupError(Exception):
    pass


class ExecutorFunctionAlreadyExistError(LineupError):
    pass


class FunctionNotExistError(LineupError):
    pass


class ExecutorFunctionNotExistError(FunctionNotExistError):
    pass


class ArgumentNotExistError(LineupError):
    pass


class DecodeLineStringError(LineupError):
    pass
