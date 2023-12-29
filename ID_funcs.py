class PylintWarning:
    """
    Pylint Warnings
    """
    def __init__(self, data):
        self.type = data.get("type")
        self.module = data.get("module")
        self.obj = data.get("obj")
        self.line = data.get("line")
        self.column = data.get("column")
        self.endLine = data.get("endLine")
        self.endColumn = data.get("endColumn")
        self.path = data.get("path")
        self.symbol = data.get("symbol")
        self.message: str or list(str) = data.get("message")
        self.message_id: str or list(str) = data.get("message-id")
    
    def __str__(self):
        return (
            f"Type: {self.type}\n"
            f"Module: {self.module}\n"
            f"Object: {self.obj}\n"
            f"Line: {self.line}\n"
            f"Column: {self.column}\n"
            f"EndLine: {self.endLine}\n"
            f"EndColumn: {self.endColumn}\n"
            f"Path: {self.path}\n"
            f"Symbol: {self.symbol}\n"
            f"Message: {self.message}\n"
            f"Message ID: {self.message_id}"
        )

class Conventions():
    def C0304(self, details: PylintWarning):
        #Newline doesn't end the code
        self.code.append('')

    def C0114(self, details: PylintWarning):
        # #https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/missing-module-docstring.html
        pass 

    def C0116(self, details: PylintWarning):
        # https://pylint.pycqa.org/en/latest/user_guide/messages/convention/missing-function-docstring.html
        pass

    def C0415(self, details: PylintWarning):
        pass

    def C0103(self, details:PylintWarning):
        # function to UPPER_CASE
        self.code[details.line-1] =  self.code[details.line-1][:-1] + "     #Constant name \"test\" doesn't conform to UPPER_CASE naming style" + self.code[details.line-1][-1]



class Warnings():
    def W0611(self, details: PylintWarning):
        #Unused Import
        self.code[details.line-1] = ""


class Errors():
    def E0001(self, details: PylintWarning):
        self.code[details.line-1] = self.code[details.line-1] + "   # {details.message}"

    def E0602(self, details: PylintWarning):
        new_string = self.code[details.line-1]
        new_string = new_string[:details.column] + '...' + new_string[details.endColumn:]
        new_string = addCommentToEnd(new_string, details.message)
        self.code[details.line-1] = new_string


class Solutions(Warnings, Conventions, Errors):
    def __init__(self, code) -> None:
        self.code: list(str) = code


def addCommentToEnd(string: str, comment: str):
    if string[-1] == "\n":
        return string[:-1] + f"     #{comment}" + string[-1]
    else:
        return string + f"     #{comment}"
    
