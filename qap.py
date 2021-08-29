from pathlib import Path
import numpy as np
import random
import math
import itertools

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

    def __init__(self, is_debug):
        self.is_debug = is_debug

    # TODO
    def move(self, currState):
        nextState = currState
        return nextState

    def eval_func(self, currState):
        """
        Evaluates the current state by
        calculating distance*flow linear combinations
        for all elements.
        """
        # element-wise linear combination of dist*flow pairs
        sums = np.zeros((3,5))

        # 3x5 array iterator
        it = np.nditer(currState, flags=['multi_index'])

        element_position = 0
        
        for x in it:
            for i in range (0,currState.shape[0]):
                for j in range (0, currState.shape[1]):
                   
                    comp_position = i + i* (currState.shape[1]-1) + j

                    if x <= currState[i][j]:
                        flow_pair = self.flow[currState[i][j]-1][x-1]
                    else:
                        flow_pair = self.flow[x-1][currState[i][j]-1]

                    dist_pair = self.dist[element_position][comp_position]
                    
                    if self.is_debug:
                        print("Comparing department {} with department {}".format(x, currState[i][j]))
                        print("Department {} position in table: {}".format(x,element_position))
                        print("Department {} position in table: {}".format(currState[i][j],comp_position))
                        print("Flow: {}, Distance: {}".format(flow_pair, dist_pair))
                        print("------------")

                    sums[it.multi_index[0]][it.multi_index[1]] += flow_pair * dist_pair

            element_position+=1

        result = np.sum(sums)

        if self.is_debug:
            print("State: \n{}\n Score: {}".format(currState, result))

        return result
    
    def sim_annealing(self,x0,t0,m,n,a, *argv):
        """
        Simulated annealing algorithm
        """

        # initialization
        x_curr = x0
        t_curr = t0
        x_final = x0

        for _ in itertools.repeat(None, m): #itertools to not generate extra variables.
            for _ in itertools.repeat(None, n):

                x_temp = self.move(x_curr)
                if self.eval_func(x_temp)<= self.eval_func(x_curr):
                    x_curr = x_temp
                else:
                    if random.uniform(0, 1) <= math.exp(-((self.eval_func(x_temp)-self.eval_func(x_curr))/t_curr)):
                        x_curr = x_temp
                    # else:
                    #     x_curr = x_curr
                if self.eval_func(x_curr) <= self.eval_func(x_final):
                    x_final = x_curr
            t_curr = a*t_curr
        return x_final


    def solve_qap(self):
        """
        Solves the qap problem.
        """
        self.flow, self.dist = parse_data()

        if self.is_debug:
            print("Flow table: \n{}".format(self.flow))
            print("Distance table: \n{}".format(self.dist))
        
        p_cooling = 0.5
        stages = 5
        moves = 3
        init_temp = 30
        init_state = np.asarray([[1,2,3,4,5],
                                [6,7,8,9,10],
                                [11,12,13,14,15]
                            ])
        # init_state = np.asarray([[9,8,13,2,1],
        #                         [11,7,14,3,4],
        #                         [12,5,6,15,10]
        #                     ])
        # solution = self.sim_annealing(x0=init_state,
        #             t0=init_temp,
        #             m=stages,
        #             n=moves,
        #             a=p_cooling)

        #debug
        solution = self.eval_func(init_state)
        #debug
        
        print ("Solution is \n{}".format(solution))


if __name__ == "__main__":
    QAP = QAP(is_debug=True)
    QAP.solve_qap()