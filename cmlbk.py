import numpy as np
from simulated_annealing import sim_annealing as sa


class CMLBK:

    def __init__(self, is_debug):
        self.is_debug = is_debug

    def move(self, currState):
        modifiers = np.random.normal(loc=0.0, scale=0.01, size=2)
        nextState = np.array([0, 0], dtype=np.float64)
        newX = currState[0] + modifiers[0]
        newY = currState[1] + modifiers[1]
        # print(modifiers)


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
    
    def solve_cmlbk(self):
        """
        Solves the 6 hump camelback function.
        """

        if self.is_debug:
           pass
        
        p_cooling = 0.99
        stages = 1000
        moves = 20
        init_temp = 1000
        init_state = np.array([0, 0], dtype=np.float64)
        
        solution = sa(x0=init_state,
                    t0=init_temp,
                    m=stages,
                    n=moves,
                    a=p_cooling,
                    move_f=self.move,
                    eval_f=self.eval_func)

        print("Solution: \n{}\n Score: {}".format(solution, self.eval_func(solution)))


if __name__ == "__main__":
    CMLBK = CMLBK(is_debug=False)
    CMLBK.solve_cmlbk()