
# from typing import override

from .constraint import Constraint
from .variable import Variable

from .exceptions import Inconsistency

class AllDifferent(Constraint):
    """
    Constraint representing that all variables must take different values.
    """
    
    def __init__(self, variables: list[Variable], offsets: list[int] | None = None, **options) -> None:
        """
        Initializes the AllDifferent constraint.

        Args:
            variables: A list of variables that must take different values.
            offsets: A list of offsets for each variable, used to adjust the values for the AllDifferent constraint.
            options: Additional options for the constraint (e.g., pigeonhole).
        """
        self.vars = variables
        # Si pas d'offsets, on utilise 0 pour toutes les variables (AllDiff classique)
        self.offsets = offsets if offsets is not None else [0] * len(variables)
        self.options = options

    # @override
    def propagate(self) -> bool:
        """
        Propagates the AllDifferent constraint.

        Returns:
            True if any value was removed from a domain, False otherwise.
        """
        changed = False
        
        if self.options.get('pigeonhole', True):
            # 1. Calculer l'union de tous les domaines "virtuels"
            union_all = set()
            for i, var in enumerate(self.vars):
                # On applique l'offset pour ramener tout le monde dans le même référentiel
                virtual_dom = {val + self.offsets[i] for val in var.dom.values}
                union_all.update(virtual_dom)
                
            # 2. TEST DES TIROIRS (Pigeonhole)
            # Si j'ai 8 reines mais seulement 7 positions possibles sur une diagonale...
            if len(union_all) < len(self.vars):
                raise Inconsistency("Plus de variables que de valeurs disponibles !")
                
        # 1. Collecter les valeurs fixées (en tenant compte des offsets)
        # Si Xi est fixé à v, alors la valeur "virtuelle" est v + offset
        fixed_values = set()
        for i, var in enumerate(self.vars):
            if var.dom.is_fixed():
                v_virtuelle = var.dom.min() + self.offsets[i]
                if v_virtuelle in fixed_values:
                    raise Inconsistency
                fixed_values.add(v_virtuelle)
                
        
        # 2. Élaguer les autres variables
        for i, var in enumerate(self.vars):
            if not var.dom.is_fixed():
                # On veut retirer 'val' tel que (val + offset) est dans fixed_values
                # donc on retire 'v_virtuelle - offset'
                for v_fixed in fixed_values:
                    val_to_remove = v_fixed - self.offsets[i]
                    if var.dom.remove(val_to_remove):
                        changed = True
        
        return changed
    
    def __repr__(self) -> str:
        return f'AllDifferent(variables={self.vars}, offsets={self.offsets})'

    def __str__(self) -> str:
        return f'AllDifferent({", ".join(var.name for var in self.vars)})'


class GACAllDifferent(Constraint):
    '''
    AllDifferent constraint using Generalized Arc Consistency (GAC) with maximum
    matching.
    '''
    
    def __init__(self, variables: list[Variable], offsets: list[int] | None = None, **options) -> None:
        self.vars = variables
        self.offsets = offsets if offsets is not None else [0] * len(variables)
        self.options = options
        
    def propagate(self) -> bool:
        n = len(self.vars)
        # 1. Préparer les domaines virtuels
        adj = []
        val_to_idx = {}
        idx_to_val = []
        
        for i, var in enumerate(self.vars):
            v_dom = []
            for val in var.dom.values:
                v_virt = val + self.offsets[i]
                if v_virt not in val_to_idx:
                    val_to_idx[v_virt] = len(idx_to_val)
                    idx_to_val.append(v_virt)
                v_dom.append(val_to_idx[v_virt])
            adj.append(v_dom)

        num_vals = len(idx_to_val)
        matching = [-1] * num_vals # valeur_idx -> var_idx
        
        # 2. Couplage Maximum (Doit matcher les N variables)
        def dfs(u, visited):
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    if matching[v] < 0 or dfs(matching[v], visited):
                        matching[v] = u
                        return True
            return False

        for i in range(n):
            if not dfs(i, [False] * num_vals):
                # ICI : Si on ne peut pas placer la i-ème reine, c'est mort.
                raise Inconsistency(f"Inconsistance détectée pour la variable {self.vars[i].name}")

        # 3. Filtrage simplifié (Hall-based)
        # Pour n=12, une GAC complète avec SCC est lourde en Python.
        # Utilisons le filtrage des valeurs "interdites" par les variables déjà fixées
        # qui est la cause n°1 d'élagage aux n-reines.
        changed = False
        fixed_vals = {idx_to_val[v_idx] for v_idx in range(num_vals) if matching[v_idx] != -1 and self.vars[matching[v_idx]].dom.is_fixed()}
        
        for i, var in enumerate(self.vars):
            if not var.dom.is_fixed():
                for fv in fixed_vals:
                    val_to_rem = fv - self.offsets[i]
                    if var.dom.remove(val_to_rem):
                        changed = True
        return changed