from collections.abc import Iterable
from .domain import Domain

class Variable:
    
    def __init__(self, dom: Iterable[int]) -> None:
        self.dom = Domain(set(dom))
        
    def value(self) -> int:
        if self.dom.is_fixed():
            return self.dom.min()
        else:
            return None
        
    
    def __repr__(self) -> str:
        return f"Variable(dom={self.dom.values})"