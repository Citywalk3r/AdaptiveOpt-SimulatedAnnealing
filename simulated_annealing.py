import itertools
import random
import math


def sim_annealing(x0,t0,m,n,a, move_f, eval_f, stopping_criterion_dict):

        """Simulated annealing algorithm

        Parameters:
            x0 : initial state array
            t0 : initial temperature
            m : temperature stages
            n : moves per stage
            a : cooling factor
            move_f : move function
            eval_f : evaluation function
            stopping_criterion_dict: The stopping criterion for the algorithm
                stopping_criterion structure: {name: val, value: val}
                Supported values for key "name" are:
                    no_improvement_over_n , no_accepted_moves_over_m
                Supported values for key "value" are:
                    any integer

        Returns:
            x_final : final state array
            state_list : list of historical states

        """

        print("Running Simulated annealing...")


        # state list of historical states (used for visualization)
        state_list = []

        # region initialization

        x_curr = x0
        t_curr = t0
        x_final = x0

        #endregion

        # If a stop criterion has been defined
        if stopping_criterion_dict is not None and stopping_criterion_dict["name"] == "no_improvement_over_n" and stopping_criterion_dict["value"]!=0:
            num_moves_without_imp = 0

            for _ in itertools.repeat(None, m):
                for _ in itertools.repeat(None, n):

                    # add the current state to the list 
                    state_list.append(x_curr)

                    x_temp = move_f(x_curr)
                    if eval_f(x_temp)<= eval_f(x_curr):
                        
                        if eval_f(x_temp)<eval_f(x_curr):
                            num_moves_without_imp = 0
                        else:
                            num_moves_without_imp +=1
                            # print("Eval: {} \n non-imp count: {} \n".format(eval_f(x_temp),num_moves_without_imp))
                        x_curr = x_temp
                    else:
                        num_moves_without_imp +=1
                        # print("Eval: {} \n non-imp count: {} \n".format(eval_f(x_temp),num_moves_without_imp))
                        if random.uniform(0, 1) <= math.exp(-(
                                                (eval_f(x_temp)-eval_f(x_curr))
                                                /t_curr)):
                            x_curr = x_temp
                    if eval_f(x_curr) <= eval_f(x_final):
                        x_final = x_curr
                    if num_moves_without_imp == stopping_criterion_dict["value"]:
                        return x_final, state_list

                t_curr = a*t_curr
            return x_final, state_list

        else:
            # vanilla algorithm
            for _ in itertools.repeat(None, m):
                for _ in itertools.repeat(None, n):

                    # add the current state to the list 
                    state_list.append(x_curr)

                    x_temp = move_f(x_curr)
                    if eval_f(x_temp)<= eval_f(x_curr):
                        x_curr = x_temp
                    else:
                        if random.uniform(0, 1) <= math.exp(-(
                                                (eval_f(x_temp)-eval_f(x_curr))
                                                /t_curr)):
                            x_curr = x_temp
                    if eval_f(x_curr) <= eval_f(x_final):
                        x_final = x_curr
                t_curr = a*t_curr
            return x_final, state_list

