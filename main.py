from lineup_lang import Language, luexec, lucore


class MyLanguage(Language):
    def __init__(self, *args, **kwargs):
        _core = []
        _core.append(lucore.VariableObject({"a": "Hello, World!"}))
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
