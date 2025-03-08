
from modeling import *

def test_not_equal():
    '''    
    >>> x = int_var(range(8))
    >>> y = int_var(range(2, 6))
    >>> post(not_equal(x, y))
    >>> x._on_fix
    StateStack([NotEqual(x=IntVar(domain=SparseSetDomain([0, 1, 2, 3, 4, 5, 6, 7]), name='Var_0'), y=IntVar(domain=SparseSetDomain([2, 3, 4, 5]), name='Var_1'))])
    >>> x
    IntVar(domain=SparseSetDomain([0, 1, 2, 3, 4, 5, 6, 7]), name='Var_0')
    >>> y
    IntVar(domain=SparseSetDomain([2, 3, 4, 5]), name='Var_1')
    >>> x.fix(3)
    >>> s = x.get_solver()
    >>> s
    TuringCP(prop_q=deque([NotEqual(x=IntVar(domain=SparseSetDomain([3]), name='Var_0'), y=IntVar(domain=SparseSetDomain([2, 3, 4, 5]), name='Var_1'))]))
    >>> s.fix_point()
    >>> y
    IntVar(domain=SparseSetDomain([2, 4, 5]), name='Var_1')
    >>> y.fix(3)
    Traceback (most recent call last):
      ...
    utils.InconsistencyException
    '''
    
    ...
    
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()