import numpy as np
import pandas as pd
from input import Input
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# input
print('Start of the Caculation Process')
input = Input()

#Load all relevant parameters into numpy format
def solve_lp():
    if input.num_of_products != 2:
        raise ValueError
    lp = linprog(c = -1 * input.cost_coef, 
                A_ub = input.resources_coef,
                b_ub = input.resources)
    return np.round(lp.x), np.round(-lp.fun)


# plot result
x, value = solve_lp()

res = []
x_max = 0
y_max = 0 
doc = []

for j, (coef, val) in enumerate(zip(input.resources_coef, input.resources)):
    limit = []
    for i in range(len(coef)):
        if coef[i] == 0:
            doc.append((j, 0) if i == 0 else (j, 1))
            limit.append(0)
        else:
            limit.append(val / coef[i])
            if i == 0:
                x_max = max(x_max, val / coef[i])
            else:
                y_max = max(y_max, val/ coef[i])
    res.append(limit)

for row, col in doc:
    res[row][col] = x_max if col == 0 else y_max

# basic setting
plt.figure(dpi = 300)
plt.xlim((0, x_max+200))
plt.ylim((0, y_max+200))
plt.xlabel(input.product_name[0])
plt.ylabel(input.product_name[1])
#plot result
linestyle = ['-', ':', '-.','--'][:len(input.resources_coef)]

for i, (li, name, style) in enumerate(zip(res, input.resource_name, linestyle)):
    if (i, 0) in doc:
        plt.hlines(li[1], xmin = 0, xmax = x_max, label = name, color ='b', linestyle = style)
    elif (i, 1) in doc:
        plt.vlines(li[0], ymin = 0, ymax = y_max, label = name, color ='b', linestyle = style)
    else:
        plt.plot([li[0], 0], [0, li[1]], label = name, color ='b', linestyle = style)

#Get the optimum point
opt_line_coef1 = -(input.cost_coef[0]/input.cost_coef[1])
opt_line_coef2 = (x[1] + (-opt_line_coef1 * x[0]))

def opt_line(x):
    return opt_line_coef1 * x + opt_line_coef2

dot = np.arange(0, x_max+10, 1/40)
plt.plot(dot, opt_line(dot), label = f'Optimum line, v = {value}', color = 'red')
plt.plot(x[0], x[1], 'go', animated = True, markersize = 6, color = 'black', label = f'Optimum points: ({x[0], x[1]})')
plt.legend()
plt.title('Graphic Solution')
plt.savefig(f'src/Linear-Progamming-Visulization/GraphicSolution/saveimgs/{input.save_name}')

#ouput a dataframe
df = pd.DataFrame({'Num of products': [{ name: v for name, v in zip(input.product_name, x)}],
                    'Value': [value]})
print(df)
print('End of Caculation Please check the downloaded png photo!')