import numpy as np
import pandas as pd
from input import Input
from utils import Basic_seeting, Construct_initial_df

# Simplex
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

def main():
    # Intialize input
    input = Input()

    # Basic Setting
    Basic_seeting()
    print('\n \nStart of the Caculation: \n')

    # Construct the tabelu
    df = Construct_initial_df()
    print('Initial Tableau: \n', df)

    simplex = Simplex(df)
    ite = 0
    max_iter = 2000


    while simplex.check_valid(df) and max_iter <= 2000:

        df, code = simplex.iterate(df)
        if code == 1:
            pass
        else:
            print('\n','The feasible is unbounded so there are no solution!')
            break

        print(f'After Iteration{ite + 1} of the algorithm: \n', df)

        ite += 1
        if ite > 2000:
            print('\n\nWarning:!!! The solution can not be found by simplex algorithm')

if __name__ == '__main__':
    main()



