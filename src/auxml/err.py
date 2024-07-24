

# Custom Exceptions

class SyntaxErrorAuXML(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        return f"AuXML Syntax Error: {self.message}"        
