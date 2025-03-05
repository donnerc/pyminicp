from turingcp.state import CopyStateManager
from turingcp.solver import TuringCP as Solver


NQueensSolution = list[int]

def nqueens(n: int = 8) -> list[NQueensSolution]:
    solutions: NQueensSolution = []
    
    cp = Solver(sm=CopyStateManager())
    q: list[IntVar] = []
    
    return solutions




'''
public class NQueens {
    public static void main(String[] args) {
        int n = 4;
        Solver cp = Factory.makeSolver(false);
        IntVar[] q = Factory.makeIntVarArray(cp, n, n);


        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) {
                cp.post(Factory.notEqual(q[i], q[j]));

                cp.post(Factory.notEqual(q[i], q[j], j - i));
                cp.post(Factory.notEqual(q[i], q[j], i - j));
                // alternative modeling using views
                // cp.post(notEqual(plus(q[i], j - i), q[j]));
                // cp.post(notEqual(minus(q[i], j - i), q[j]));

            }



        DFSearch search = Factory.makeDfs(cp, () -> {
            int idx = -1; // index of the first variable that is not fixed
            for (int k = 0; k < q.length; k++)
                if (q[k].size() > 1) {
                    idx = k;
                    break;
                }
            if (idx == -1)
                return new Procedure[0];
            else {
                IntVar qi = q[idx];
                int v = qi.min();
                Procedure left = () -> cp.post(Factory.equal(qi, v));
                Procedure right = () -> cp.post(Factory.notEqual(qi, v));
                return new Procedure[]{left, right};
            }
        });

        search.onSolution(() ->
                System.out.println("solution:" + Arrays.toString(q))
        );
        SearchStatistics stats = search.solve(statistics -> statistics.numberOfSolutions() == 1000);

        //search.showTree("NQUEENS");

        System.out.format("#Solutions: %s\n", stats.numberOfSolutions());
        System.out.format("Statistics: %s\n", stats);

    }
}

'''