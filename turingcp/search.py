import collections.abc
from typing import Any


from state_types import StateManager
from util_types import Predicate, Supplier, Procedure
from cp_types import CPSolver

from state import NewState

from utils import StopSearchException
from utils import InconsistencyException
from constraint import NotEqual, Equal
from variable import IntVarImpl


type BranchingStrategy = Supplier[list[Procedure]]


class SearchStatistics:
    """
    Class to store and manage search statistics.
    """

    def __init__(self) -> None:
        self.n_failures: int = 0
        self.n_nodes: int = 0
        self.n_solutions: int = 0
        self.completed: bool = False

    def __str__(self) -> str:
        return (
            "\n\t#choice: "
            + str(self.n_nodes)
            + "\n\t#fail: "
            + str(self.n_failures)
            + "\n\t#sols : "
            + str(self.n_solutions)
            + "\n\tcompleted : "
            + str(self.completed)
            + "\n"
        )

    def incr_failures(self) -> None:
        self.n_failures += 1

    def incr_nodes(self) -> None:
        self.n_nodes += 1

    def incr_solutions(self) -> None:
        self.n_solutions += 1

    def set_completed(self) -> None:
        self.completed = True

    def number_of_failures(self) -> int:
        return self.n_failures

    def number_of_nodes(self) -> int:
        return self.n_nodes

    def number_of_solutions(self) -> int:
        return self.n_solutions

    def is_completed(self) -> bool:
        return self.completed


class DFSearch:

    def __init__(self, solver: CPSolver, branching: BranchingStrategy | None) -> None:
        self.solver: CPSolver = solver
        self.sm: StateManager = solver.get_state_manager()
        self.branching: BranchingStrategy = branching or self.default_branching()
        self.cur_node_id: int = -1

        # collects all handlers (args beginning with `on_`)
        self.handlers = {}

    def default_branching(self) -> BranchingStrategy:
        def strategy():
            def left():
                self.solver.post(Equal(var, IntVarImpl(self.solver, {v})))

            def right():
                self.solver.post(NotEqual(var, IntVarImpl(self.solver, {v})))

            # next variable choice
            for var in self.solver.vars:
                if not var.is_fixed():
                    break
            else:
                return []

            # next value choice
            v: int = var.min()

            return [left, right]
        return strategy
    

    def solve(self, limit: Predicate[SearchStatistics] | None = None
    ) -> SearchStatistics:
        limit = limit or (lambda stats: False)
        stats: SearchStatistics = SearchStatistics()
        self.cur_node_id = 0

        with NewState(self.sm):
            try:
                self.dfs(stats, limit, -1, -1)
                stats.set_completed()
            except StopSearchException as ignored:
                ...
            except RecursionError as e:
                print(
                    "Try increasing the recursion limit with `sys.setrecursionlimit(limit)`"
                )
                print("or ... implement DFS using an explicit stack")

        return stats

    def dfs(
        self,
        stats: SearchStatistics,
        limit: Predicate[SearchStatistics],
        parent_id: int,
        position: int,
    ) -> None:
        if limit(stats):
            raise StopSearchException

        branches: list[Procedure] = self.branching()
        self.cur_node_id += 1
        node_id: int = self.cur_node_id

        if len(branches) == 0:
            stats.incr_solutions()
            self.call_handlers(
                "solution",
                {"parent_id": parent_id, "node_id": node_id, "position": position},
            )
        else:
            self.call_handlers(
                "branch",
                {
                    "parent_id": parent_id,
                    "node_id": node_id,
                    "position": position,
                    "n_childs": len(branches),
                },
            )
            pos: int = 0
            for branch in branches:
                with NewState(self.sm):
                    try:
                        stats.incr_nodes()
                        branch()
                        self.dfs(stats, limit, node_id, pos)
                    except InconsistencyException as e:
                        self.cur_node_id += 1
                        stats.incr_failures()
                        self.call_handlers(
                            "failure",
                            {
                                "parent_id": parent_id,
                                "node_id": node_id,
                                "position": position,
                            },
                        )
                pos += 1

    ############ Event handler registration and management
    def register_handler(self, event, handler) -> None:
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]

    def call_handlers(self, event: str, infos: dict[str, Any]) -> None:
        if event in self.handlers:
            handlers = self.handlers[event]
            for h in handlers:
                h(self, infos)

    def on(self, *events):
        def decorator(func):
            for event in events:
                self.register_handler(event, func)

        return decorator

    def on_solution(self, handler) -> None:
        self.register_handler("solution", handler)

    def on_failure(self, handler) -> None:
        self.register_handler("failure", handler)

    def on_branch(self, handler) -> None:
        self.register_handler("branch", handler)

    ###############################################################

    def branching_strategy(self, func: BranchingStrategy):
        def wrapper():
            self.branching = func

        return wrapper
