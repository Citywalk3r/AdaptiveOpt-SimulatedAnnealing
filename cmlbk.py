import numpy as np
from simulated_annealing import sim_annealing as sa


class CMLBK:

    def __init__(self, is_debug):
        self.is_debug = is_debug

    def move(self, currState):
        """Samples 2 values from a normal distribution with mean=0 and std=0.001
           Adds the first value to x and the second to y, if the new numbers
           remain within the bounds (i.e., x E (-3,3) and y E (-2,2)).
        """

        nextState = np.copy(currState)
        modifiers = np.random.normal(loc=0.0, scale=0.001, size=2)
        newX = currState[0] + modifiers[0]
        newY = currState[1] + modifiers[1]


        if newX > -3 and newX < 3:
            nextState[0] = newX
        if newY > -2 and newY < 2:
            nextState[1] = newY

        return nextState

    def eval_func(self, currState):
        """
        Evaluates the current state by
        calculating the function result.
        """

        x = currState[0]
        y = currState[1]
        z = (4 - 2.1 * x**2 + (x**4)/3) * x**2 + x * y + (-4 + 4 * y**2) * y**2
        return z
    
    def solve_cmlbk(self, init_state=None, stop_crit_dict=None):
        """
        Solves the 6 hump camelback function.
        """

        # list of historical state evaluations
        eval_list = []

        p_cooling = 0.99
        stages = 5000
        moves = 1
        init_temp = 0.01

        if init_state is not None:
            init_state = np.array(init_state, dtype=np.float64)
        else:
            init_state = np.array([0, 0], dtype=np.float64)
        
        
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
                delta_e = abs(e-previous_e)
                sum_delta_e += delta_e
            previous_e = e
            currState = self.move(currState)

        avg_delta_e = sum_delta_e/(num_moves-1)
        return ("CMLBK: Chosen initial temperature {} gives: {} probability to accept a non-improving move.".format(t_test, math.exp(-(avg_delta_e/t_test))))


if __name__ == "__main__":
    CMLBK = CMLBK(is_debug=False)
    CMLBK.solve_cmlbk()