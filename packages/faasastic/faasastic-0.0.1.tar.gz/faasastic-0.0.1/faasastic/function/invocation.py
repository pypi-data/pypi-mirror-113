
class Invocation:
    def __init__(self, invokerId: str, functionName: str, functionArgs: dict) -> None:
        self.invokerId = invokerId
        self.functionName = functionName
        self.functionArgs = functionArgs

class InvocationResult:
    def __init__(self, functionResult: dict) -> None:
        self.functionResult = functionResult

