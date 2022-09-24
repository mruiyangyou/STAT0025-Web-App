import numpy as np
from scipy.optimize import linprog

class input(object):

    cost_coef = np.array([3, 8])
    resources_coef = np.array([[2, 4], [6,2], [0,1]])
    resources = np.array([1600, 1800, 350])

def solve_lp():
    lp = linprog(c = -1 * input.cost_coef, 
                A_ub = input.resources_coef,
                b_ub = input.resources)
    return np.round(lp.x), np.round(-lp.fun)

x, res = solve_lp()

print(x, res)