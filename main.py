from lineup import Language
from lineup.executor import JumperExecutor
import lineup.core as core


class MyLanguage(Language):
    def __init__(self):
        _core = []
        _core.append(core.VariableObject({"a": "Hello, World!"}))
        executor = JumperExecutor(_core)
        super().__init__(executor)


language = MyLanguage()
result = language.execute_script("VAR a GET")
print(result)
result = language.execute_script("""
VAR c SET "Hello, World!"
JUMP 2
VAR b SET "Hello, Worls!"
VAR b GET
""")
print(result)
