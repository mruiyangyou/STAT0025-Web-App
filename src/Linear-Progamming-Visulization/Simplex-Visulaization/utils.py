import numpy as np
import pandas as pd
from input import Input

input = Input()

def Construct_initial_df():
    num = input.num_of_products
    num_con = len(input.resources)
    df1 = pd.DataFrame(input.resources_coef, columns=[f'X{i + 1}' for i in range(num)])

    df2_col_name = [f'X{i + 1}' for i in range(num, num + num_con)]
    df2_value = np.zeros((num_con, num_con))
    np.fill_diagonal(df2_value, val = 1)
    df2 = pd.DataFrame(df2_value, columns=df2_col_name)

    df3 = pd.DataFrame({'Sol': input.resources})
    df = pd.concat([df1, df2, df3], axis=1)

    df4_val = list(map(lambda x: -x, input.cost_coef)) + [0] * (num_con + 1)
    df4 = pd.DataFrame({col: [val] for col, val in zip(df.columns.tolist(), df4_val)})

    df = pd.concat([df, df4], axis=0)
    df.index = df2_col_name + ['z']
    return df


def Basic_seeting():
    # Basic Setting
    obj = 'Maximise' if input.objective == 'max' else 'Minimize'
    obj_func = []

    # print Objective function
    for i in range(1, input.num_of_products + 1):
        obj_func.append(f'{input.cost_coef[i - 1]}X{i}')
    obj_fun = ' + '.join(obj_func)
    print(obj + ':  z = ' + obj_fun)

    # print Constrint function
    constraint_func = []
    for i in range(len(input.resources_coef)):
        c_func = []
        for j in range(1, input.num_of_products + 1):
            c_func.append(f'{input.resources_coef[i][j - 1]}X{j}')
        constraint_func.append(c_func)

    for num in range(len(constraint_func)):
        if num == 0:
            print('Such that: ', ' + '.join(constraint_func[num]), f' <= {input.resources[num]}')
        else:
            print('           ', ' + '.join(constraint_func[num]), f' <= {input.resources[num]}')