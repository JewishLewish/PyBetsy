import json
import subprocess
from ID_funcs import Solutions, PylintWarning

TOMBSTONE = "🪦"

class Codegen(Solutions):
    def __init__(self, code, warnings):
        super().__init__(code=code)
        self.warnings: set[PylintWarning] = set(warnings)
    
    def removeRepeats(self):
        new_Warnings = []
        warnings_data_list = []

        for warning in self.warnings:
            data = {"line":warning.line, "column":warning.column, "endLine":warning.endLine}
            if data in warnings_data_list:
                pass
            else:
                warnings_data_list.append(data)
                new_Warnings.append(warning)
    
        self.warnings = set(new_Warnings)

    def review(self):
        for warning in self.warnings:
            try:
                function_reference = getattr(self, warning.message_id)
                try:
                    function_reference(warning)
                except Exception as e:
                    print(e)
            except:
                print("WARNING MESSAGE ID =>", warning.message_id, "<= IS NOT IMPLEMENTED!")
    
    def writeTo(self, target_file):
        with open("new"+target_file, "w") as f:
            f.write(''.join(code.code))

def run_pylint(args): subprocess.run(["pylint"] + args, capture_output=True, text=True) 

def read_content(target_file) -> str:
    with open(target_file, "r") as f: return f.read()

def read_python_content(target_file) -> str:
    with open(target_file, "r") as f: return f.readlines()


if __name__ == "__main__":
    target_file = "main.py"
    run_pylint([target_file, "--output-format=json:review.json"])
    
    code = Codegen(read_python_content(target_file), set([PylintWarning(message) for message in json.loads(read_content("review.json"))]))
    code.removeRepeats()
    code.review()
    print("================")
    print(''.join(code.code))
    code.writeTo(target_file=target_file)
