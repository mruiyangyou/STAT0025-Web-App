import numpy as np
import pandas as pd
from input import Input

input = Input()

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
            print('Such that: ', ' + '.join(constraint_func[num]), f' {input.constraint_char[num]} {input.resources[num]}')
        else:
            print('           ', ' + '.join(constraint_func[num]), f' {input.constraint_char[num]} {input.resources[num]}')

    print('\n\nThe artificial probelm is')

    # title
    artifical = {}
    artifical_idx = 1
    help = {}
    help_idx = input.num_of_products + 1
    for j, char in enumerate(input.constraint_char):
        if char not in ['<=','<']:
            artifical[j] = f'Y{artifical_idx}'
            artifical_idx += 1
        help[j] = f'X{help_idx}'
        help_idx += 1
    artifical_title = '(' + ' + '.join([char for char in artifical.values()]) + ')'

    print(obj + ':  z = ' + obj_fun + ' -M' + artifical_title)

    for num in range(len(constraint_func)):
        if num in artifical.keys():
            print('          ', ' + '.join(constraint_func[num]), f' - {help[num]} + {artifical[num]}', f' = {input.resources[num]}')
        else:
            print('          ', ' + '.join(constraint_func[num]),f' + {help[num]}', f' = {input.resources[num]}')

    return artifical, help


def Construct_initial_df(artifical, help):
    num = input.num_of_products
    num_con = len(input.resources)
    df1 = pd.DataFrame(input.resources_coef, columns=[f'X{i + 1}' for i in range(num)])

    df2_col_name = [f'X{i + 1}' for i in range(num, num + num_con)]
    df2_value = np.zeros((num_con, num_con))
    np.fill_diagonal(df2_value, val = 1)
    df2 = pd.DataFrame(df2_value, columns=df2_col_name)
    for idx in artifical.keys():
        df2.loc[idx, help[idx]] = -1

    df3_col_name = list(artifical.values())
    df3_value = { col: [0] * num_con  for col in df3_col_name }
    df3 = pd.DataFrame(df3_value, columns=df3_col_name)
    for idx, j in artifical.items():
        df3.loc[idx, j] = 1

    df4 = pd.DataFrame({'Sol': input.resources})
    df = pd.concat([df1, df2, df3, df4], axis=1)

    df4_val = list(map(lambda x: -x, input.cost_coef)) + [0] * (num_con + 1 + len(artifical))
    df4 = pd.DataFrame({col: [val] for col, val in zip(df.columns.tolist(), df4_val)})
    df4[df3_col_name] = float('inf')

    df = pd.concat([df, df4], axis=0)
    df_col_name = [artifical[idx] if idx in artifical.keys() else col for idx, col in help.items()] + ['z']
    df.index = df_col_name
    return df

# artifical, help =Basic_seeting()
# print(Construct_initial_df(artifical, help))