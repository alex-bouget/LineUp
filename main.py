from lineup_lang import Language, luexec, lucore


class MyLanguage(Language):
    def __init__(self, *args, **kwargs):
        _core = []
        _core.append(lucore.Variables({
            "a": "Hello, World!",
            "b": "Hello, WorldB!"
        }))
        _core.append(lucore.Conditions())
        _core.append(lucore.System())
        executor = luexec.JumperExecutor(_core)
        super().__init__(executor, *args, **kwargs)


language = MyLanguage(no_error=True, log_level="DEBUG")
result = language.execute_script(
    """
    VAR c USE VAR a GET
    VAR c GET
    """)
print(result)
result = language.execute_script(
    """
    VAR c GET
    """)
print(result)
result = language.execute_script(
    """
    JUMP 2
    VAR c USE VAR a GET
    EXIT VAR c GET
    """
)
print(result)
result = language.execute_script(
    """
    VAR c USE VAR a GET
    IF *+2 VAR c GET
    ELSE *+2
    EXIT VAR a GET
    EXIT VAR b GET
    """
)
print(result)
result = language.execute_script(
    """
    VAR c USE VAR a GET
    IF *+2 "VAR a GET" EQ "VAR c GET"
    ELSE *+2 FROM
    EXIT VAR a GET
    EXIT VAR b GET
    """
)
print(result)

print(language.get_versions())
