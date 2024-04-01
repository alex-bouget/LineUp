from lineup_lang import Language
from lineup_lang.executor import JumperExecutor
import lineup_lang.core as core


class MyLanguage(Language):
    def __init__(self, *args, **kwargs):
        _core = []
        _core.append(core.VariableObject({"a": "Hello, World!"}))
        executor = JumperExecutor(_core)
        super().__init__(executor, *args, **kwargs)


language = MyLanguage(True)
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
