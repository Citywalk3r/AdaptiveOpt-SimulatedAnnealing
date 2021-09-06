from pathlib import Path
import numpy as np
from simulated_annealing import sim_annealing as sa


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
        self.flow, self.dist = parse_data()

    def move(self, currState):
        """Implements the move operator.
           Picks 2 random elements from the array and swaps them.
        """

        nextState = np.array(currState.flatten())

        # Randomly select two elements from the array (An element cannot be picked twice)
        swap_pair = np.random.choice(nextState.size, size=2, replace=False)

        #Swap the selected elements
        nextState[swap_pair[0]], nextState[swap_pair[1]] = nextState[swap_pair[1]], nextState[swap_pair[0]]

        return nextState.reshape(3,5)

    def eval_func(self, currState):
        """
        Evaluates the current state by
        calculating distance*flow linear combinations
        for all elements.

        --performance bottleneck--
        """
        sums = np.zeros((3,5))

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

        return np.sum(sums)
    
    def solve_qap(self, init_state=None, stop_crit_dict=None):
        """
        Solves the qap problem.
        """

        # list of historical state evaluations
        eval_list = []

        if self.is_debug:
            print("Flow table: \n{}".format(self.flow))
            print("Distance table: \n{}".format(self.dist))
        
        p_cooling = 0.99
        stages = 1000
        moves = 5
        init_temp = 30

        if init_state is not None:
            init_state = np.asarray(init_state)
        else:
            init_state = np.asarray([[1,2,3,4,5],
                        [6,7,8,9,10],
                        [11,12,13,14,15]
                    ])
        
        solution, statelist = sa(x0=init_state,
                    t0=init_temp,
                    m=stages,
                    n=moves,
                    a=p_cooling,
                    move_f=self.move,
                    eval_f=self.eval_func,
                    stopping_criterion_dict=stop_crit_dict)
        
        for state in statelist:
            eval_list.append(self.eval_func(state))

        score = self.eval_func(solution)
        print("Solution: \n{}\n Score: {}".format(solution, score))

        import matplotlib.pyplot as plt

        plt.plot(range(len(eval_list)), eval_list)
        plt.xlabel("iterations")
        plt.ylabel("score")
        plt.show()
        

        return init_state, solution, score, init_temp, stages, moves, p_cooling

    def calculate_init_temp(self, num_moves, init_state, t_test):
        import itertools
        import math
        currState = init_state
        previous_e = None
        sum_delta_e = 0
        for _ in itertools.repeat(None, num_moves):
            e = self.eval_func(currState)
            if previous_e:
                delta_e = abs(e - previous_e)
                sum_delta_e += delta_e
            previous_e = e
            currState = self.move(currState)

        avg_delta_e = sum_delta_e/(num_moves-1)
        return ("QAP: Chosen initial temperature {} gives: {} probability to accept a non-improving move.".format(t_test, math.exp(-(avg_delta_e/t_test))))
            
if __name__ == "__main__":
    QAP = QAP(is_debug=False)
    QAP.solve_qap()