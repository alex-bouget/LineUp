from lineup_lang import Language, luexec, lucore


class MyLanguage(Language):
    def __init__(self, *args, **kwargs):
        _core = []
        _core.append(lucore.VariableObject({
            "a": "Hello, World!",
            "b": "Hello, WorldB!"
        }))
        _core.append(lucore.ConditionsJumpObject())
        executor = luexec.JumperExecutor(_core)
        super().__init__(executor, *args, **kwargs)


language = MyLanguage(no_error=True, log_level="DEBUG")
result = language.execute_script(
    """
    VAR c COPY a
    """)
print(result)
result = language.execute_script(
    """
    VAR c GET
    """)
print(result)
result = language.execute_script(
    """
    JUMP 3
    VAR c COPY a
    EXIT VAR c GET
    """
)
print(result)
result = language.execute_script(
    """
    VAR c COPY a
    IF 1 FROM VAR c GET
    ELSE 1 FROM
    EXIT VAR a GET
    EXIT VAR b GET
    """
)
print(result)
