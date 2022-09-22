import numpy as np
import pandas as pd
import time
import os
# Construct input class
class SimplexInput(object):

     def __init__(self, cost_coef, resources_coef, resources, objective,
                    num_of_products) -> None:
        self.cost_coef = cost_coef
        self.resources_coef = resources_coef
        self.resources = resources
        self.objective = objective
        self.num_of_products = num_of_products

# Construct the intial tableau
def Construct_initial_df(input):
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


# Construct a simplex class
class Simplex(object):

    def __init__(self, df):
        self.df = df

    def check_valid(self, df):
        z = df.loc['z']
        return any(z.values < 0)

    def iterate(self, df):

        # set the code
        code = 1

        # Get the col need to be added
        col = df.columns.to_list()[np.argmin(df.loc['z'].values)]  # 'x2'

        # Calulcate the theta
        def cal_theta(x, y):
            return y / x if x > 0 else -float('inf')

        df['theta'] = df.apply(lambda x: cal_theta(x[col], x['Sol']), axis = 1)

        # check whether unbound exist
        if all(df['theta'].values <= 0):
            code = 2
            return df, code

        # Find the exit idx
        postive_theta = df['theta'].values[df['theta'].values > 0]
        postive_idx = df.index[df['theta'].values > 0]
        exit_idx = postive_idx.to_list()[np.argmin(postive_theta)]
        exit_val = df.loc[exit_idx, col] if df.loc[exit_idx, col] > 0 else \
            -df.loc[exit_idx, col]
        df.loc[exit_idx] = df.loc[exit_idx].div(exit_val)
        remain_idx = df.index.to_list()
        index_idx = remain_idx.index(exit_idx)
        # remain_idx.remove(exit_idx)
        for i, idx in enumerate(remain_idx):
            if i != index_idx:
                val = df.loc[idx, col]
                df.loc[idx] = (df.loc[idx] - df.loc[exit_idx].mul(val)) # if val >= 0 else (df.loc[idx] + df.loc[exit_idx].mul(val))
            else:
                pass
        remain_idx[index_idx] = col
        df.index = remain_idx
        df.drop(columns = ['theta'], inplace = True)
        return df, code

def Simplex_loop(input, path):
    # # Intialize input
    # input = Input()

    # # Basic Setting
    # Basic_seeting()
    # print('\n \nStart of the Caculation: \n')
    
    file_name = time.strftime('simplex_' + '%m%d_%H:%M:%S.xlsx')
    path = os.path.join(path, file_name)
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

    # Construct the tabelu
    df = Construct_initial_df(input)
    df.to_excel(writer, sheet_name='initial tableau')

    simplex = Simplex(df)
    ite = 0
    max_iter = 2000
   

    while simplex.check_valid(df) and max_iter <= 2000:

        df, code = simplex.iterate(df)
        if code == 1:
            df.to_excel(writer, sheet_name=f'{ite + 1} tableau')
            output = 'Successfully Calculated'
        else:
            output = 'The feasible is unbounded so there are no solution!'
            break

        # print(f'After Iteration{ite + 1} of the algorithm: \n', df)

        ite += 1
        if ite > 2000:
            # print('\n\nWarning:!!! The solution can not be found by simplex algorithm')
            output = 'Warning:!!! The solution can not be found by simplex algorithm'

    writer.save()
    writer.close()

    return output, file_name