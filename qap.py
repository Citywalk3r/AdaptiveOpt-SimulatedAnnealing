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

    def move(self, currState):

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

        return np.sum(sums)
    
    def solve_qap(self):
        """
        Solves the qap problem.
        """
        self.flow, self.dist = parse_data()

        if self.is_debug:
            print("Flow table: \n{}".format(self.flow))
            print("Distance table: \n{}".format(self.dist))
        
        p_cooling = 0.99
        stages = 1000
        moves = 5
        init_temp = 1000
        init_state = np.asarray([[1,2,3,4,5],
                                [6,7,8,9,10],
                                [11,12,13,14,15]
                            ])
        
        solution = sa(x0=init_state,
                    t0=init_temp,
                    m=stages,
                    n=moves,
                    a=p_cooling,
                    move_f=self.move,
                    eval_f=self.eval_func)

        print("Solution: \n{}\n Score: {}".format(solution, self.eval_func(solution)))

        return

        #region Examples

        # eval 702
        ex_1 = np.asarray([[10,5,8,7,12],
                               [9,6,13,2,4],
                               [15,3,14,1,11]
                            ])

        # eval 713
        ex_2 = np.asarray([[7,10,14,2,1],
                               [12,8,6,4,13],
                               [5,15,11,3,9]
                            ])

        # eval 647
        ex_3 = np.asarray([[10,12,8,9,11],
                               [6,5,3,13,1],
                               [15,4,14,2,7]
                            ])

        # eval 575 - optimal
        ex_4 = np.asarray([[9,8,13,2,1],
                                [11,7,14,3,4],
                                [12,5,6,15,10]
                            ])

        #endregion


if __name__ == "__main__":
    QAP = QAP(is_debug=False)
    QAP.solve_qap()