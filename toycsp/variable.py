from collections.abc import Iterable
from .domain import Domain

class Variable:

    var_counter = 0
    
    def __init__(self, dom: Iterable[int], name: str = None) -> None:
        self.dom = Domain(set(dom))
        self.name = name or 'Var' + str(Variable.var_counter)
        Variable.var_counter += 1
        
    def value(self) -> int:
        if self.dom.is_fixed():
            return self.dom.min()
        else:
            return None
        
    
    def __repr__(self) -> str:
        return f"Variable(dom={self.dom.values}, name='{self.name}')"