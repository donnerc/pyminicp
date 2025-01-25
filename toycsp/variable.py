from .domain import Domain

class Variable:
    
    def __init__(self, n: int) -> None:
        self.dom = Domain(n)
        
    