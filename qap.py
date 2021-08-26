from pathlib import Path
import numpy as np
import random
import math

def parse_data():
    data_file = Path("flow_dist_tbl.csv")
    try:
        data_file.resolve(strict=True)
    except FileNotFoundError:
        print ("flow_dist_tbl.csv not found. Please include the data file in the root folder. Aborting..\n")
        return
    else:
        data = np.genfromtxt(data_file, dtype=int, delimiter=',')
        return np.tril(data), np.triu(data)




class QAP:

    def __init__(self, is_debug=False):
        self.is_debug = is_debug

    # TODO
    def move(self, currState):
        nextState = currState
        return nextState

    def eval_func(self, currState):
        """
        Minimization is the objective.
        A lower returned value is better 
        """
        sums = np.empty()

        
        it = np.nditer(currState, flags=['multi_index'])

        for x in it:
            for i in range (it.multi_index[0],currState.shape[0]):
                for j in range (it.multi_index[1], currState.shape[1]):
                    sums[it.multi_index[0]][it.multi_index[1]] += self.flow[currState[i][j]][x]*self.dist[x][i+j]
        result = np.sum(sums)
        return result
    
    def sim_annealing(self, x0,t0,m,n,a, *argv):
        """
        Simulated annealing algorithm
        """

        # initialization
        X = np.array(n)
        T = np.array(m)
        X[1] = x0
        T[1] = t0
        Xf = x0

        for t in range(1,m):
            for i in range(1,n):
                Xtemp = self.move(X[i])
                if self.eval_func(Xtemp)<= self.eval_func(X[i]):
                    X[i+1] = Xtemp
                else:
                    if random.uniform(0, 1) <= math.exp(-((self.eval_func(Xtemp)-self.eval_func(X[i]))/T[t])):
                        X[i+1] = Xtemp
                    else:
                        X[i+1] = X[i]
                if self.eval_func(X[i+1]) <= self.eval_func(Xf):
                    Xf = X[i+1]
            T[t+1] = a*T[t]
        return Xf


    def solve_qap(self):
        """
        Solves the qap problem.
        """
        self.flow, self.dist = parse_data()

        if self.is_debug:
            print(self.flow)
            print("----------------")
            print(self.dist)
        
        p_cooling = 0.5
        stages = 5
        moves = 5
        init_temp = 30
        init_state = np.asarray([[1,2,3,4,5],
                                [6,7,8,9,10],
                                [11,12,13,14,15]
                            ])
        solution = sim_annealing(x0=init_state,
                    t0=init_temp,
                    m=stages,
                    n=moves,
                    a=p_cooling)
        
        print ("Solution is {}".format(solution))


if __name__ == "__main__":
    QAP = QAP(is_debug=True)
    QAP.solve_qap()