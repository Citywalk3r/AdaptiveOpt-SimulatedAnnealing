import itertools
import random
import math

def sim_annealing(x0,t0,m,n,a, move_f, eval_f):

        """Simulated annealing algorithm

        Parameters:
            x0 : initial state array
            t0 : initial temperature
            m : temperature stages
            n : moves per stage
            a : cooling factor
            move_f : move function
            eval_f : evaluation function

        Returns:
            x_final : final state array

        """

        print("Running Simulated annealing...")

        # region initialization
        
        x_curr = x0
        t_curr = t0
        x_final = x0

        #endregion

        for _ in itertools.repeat(None, m):
            for _ in itertools.repeat(None, n):

                x_temp = move_f(x_curr)
                if eval_f(x_temp)<= eval_f(x_curr):
                    x_curr = x_temp
                else:
                    if random.uniform(0, 1) <= math.exp(-((eval_f(x_temp)-eval_f(x_curr))/t_curr)):
                        x_curr = x_temp
                if eval_f(x_curr) <= eval_f(x_final):
                    x_final = x_curr
            t_curr = a*t_curr
        return x_final

