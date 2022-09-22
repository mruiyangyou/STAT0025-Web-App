import numpy as np
import pandas as pd


class MarkovDp(object):
    def __init__(self, reward_matrix, terminal_reward, action_tm):
        self.num_of_states = action_tm.shape[1]
        self.num_of_actions = action_tm.shape[0]
        self.reward_matrix = reward_matrix
        self.terminal_reward = terminal_reward
        self.action_tm = action_tm
        self.state = [i for i in range(self.num_of_states)]
        self.action = [j for j in range(self.num_of_actions)]
        self.total = self.num_of_states * self.num_of_actions

    def get_reward_df(self, n, alpha):
        colname = ['n', 'state', 'action', 'R_n', 'V_n(-1)', 'sum', 'V_best', 'Action_best']
        rownum = self.num_of_states + n * self.num_of_states * self.num_of_actions

        df = pd.DataFrame(np.zeros((rownum, len(colname))), columns=colname)
        for i in range(self.num_of_states):
            df.loc[i, 'n'] = 0
            df.loc[i, 'state'] = i
            df.loc[i, 'R_n'], df.loc[i, 'sum'], df.loc[i, 'V_best'] = self.terminal_reward[i], self.terminal_reward[i], \
                                                                      self.terminal_reward[i]

        v_best = df.loc[0:self.num_of_states - 1, 'V_best'].to_numpy()
        print(v_best)
        for i in range(1, n + 1):
            if i > 1:
                #v_best = df.loc[self.num_of_states * i:self.num_of_states * i + self.total - 1:self.num_of_actions,'V_best'].to_numpy()
                v_best = df.loc[self.num_of_states+(i-2)*self.total:self.num_of_states+(i-1) * self.total - 1 : self.num_of_actions, 'V_best'].to_numpy()
                # print(v_best)
            for j in range(self.num_of_states):
                for z in range(self.num_of_actions):
                    row = self.num_of_states + self.total * (i-1) + j * self.num_of_actions + z
                    df.loc[row, 'n'] = i
                    df.loc[row, 'state'] = j
                    df.loc[row, 'action'] = z
                    df.loc[row, 'R_n'] = np.sum(
                        self.reward_matrix[z, j, :] * self.action_tm[z, j, :])
                    df.loc[row, 'V_n(-1)'] = alpha*np.sum(
                        self.action_tm[z, j, :] * v_best)
                    df.loc[row, 'sum'] = df.loc[row, 'R_n'] + df.loc[row, 'V_n(-1)']
                    if z == self.num_of_actions - 1:
                        lower = row + 1 - self.num_of_actions
                        upper = row
                        v = df.loc[lower:upper, 'sum'].max(axis=0)
                        df.loc[lower:upper, 'V_best'] = v
                        action_df = df.loc[lower:upper]
                        #print(action_df)
                        #print(v)
                        action_best = action_df.loc[action_df['sum'] == v, 'action'].to_list()
                        #print(action_best)

                        if len(action_best) > 1:
                            action_best = 'or'.join([str(x) for x in action_best])
                        else:
                            action_best = action_best[0]
                        df.loc[lower:upper, 'Action_best'] = action_best

        return df
