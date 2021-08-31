import qap
import cmlbk
from time import process_time
import numpy as np

def set_init_QAP_states():

    initial_states = []
     
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

    # eval 663
    ex_4 = np.asarray([[9,8,13,2,12],
                        [11,7,14,3,4],
                        [1,5,6,15,10]
                    ])

    # eval 746
    ex_5 = np.asarray([[1,2,3,4,5],
                        [6,7,8,9,10],
                        [11,12,13,14,15]
                    ])
    
    # eval 575 - optimal
    ex_6 = np.asarray([[9,8,13,2,1],
                        [11,7,14,3,4],
                        [12,5,6,15,10]
                    ])
    
    initial_states.extend([ex_1,ex_2,ex_3,ex_4,ex_5])
    return initial_states

def set_init_CMLBK_states():

    initial_states = []
    ex_1= [-1, 1]
    ex_2= [-1.5, 1.5]
    ex_3= [0, 0]
    ex_4= [1.5, 1.95]
    ex_5= [-0.55, 0]
    initial_states.extend([ex_1,ex_2,ex_3,ex_4,ex_5])


    return initial_states

def generte_stopping_criteria(val_crit_1, val_crit_2):
    """
        Generates the list of stopping criteria.
        Criteria are represented as dictionarys with 2 key-value pairs:

        1) Name of the criterion
        2) Value of the criterion
       
      Parameters:
            val_crit_1 : The value for no_improvement_over_n criterion.
            val_crit_2 : The value for no_accepted_moves_over_m criterion.

        Returns:
            stopping_criteria : List of 2 dictionaries, 1 for each criterion

    """

    stopping_criteria = []
    stopping_criterion_vanilla_algorithm = None
    stopping_criterion_no_imp = {"name": "no_improvement_over_n", "value": val_crit_1}
    stopping_criterion_no_acc = {"name": "no_accepted_moves_over_m", "value": val_crit_2}
    stopping_criteria.extend([stopping_criterion_vanilla_algorithm, stopping_criterion_no_imp, stopping_criterion_no_acc])
    return stopping_criteria


def main_menu():
    print_str = """Welcome to Adaptive Optimization HW_1: Simulated Annealing\n
            The available problems are the following:\n
            1) Combinatorial Optimization -- QAP\n
            2) Continuous Optimization: 6 hump camelback function\n
            3) Both problems (45 runs with different starting points, schedules and stopping criteria).
            """
    print(print_str)
    try:
        selection = input("Please type 1 or 2 or 3 and press ENTER...\n")
        while selection!="1" and selection!="2" and selection!="3":
            selection = input("Invalid choice. Please type 1 or 2 or 3 and press ENTER...\n")
        if selection=="1":
            QAP = qap.QAP(is_debug=False)
            t = process_time()
            QAP.solve_qap()
            elapsed_time = process_time() - t
            print("Elapsed time: {} seconds.".format(elapsed_time))
        elif selection=="2":
            CMLBK = cmlbk.CMLBK(is_debug=False)
            t = process_time()
            CMLBK.solve_cmlbk()
            elapsed_time = process_time() - t
            print("Elapsed time: {} seconds.".format(elapsed_time))
        else:

            stopping_criteria = generte_stopping_criteria()
            initial_QAP_states = set_init_QAP_states()
            initial_CMLBK_states = set_init_CMLBK_states()
            QAP = qap.QAP(is_debug=False)
            CMLBK = cmlbk.CMLBK(is_debug=False)

            for stop_criterion in stopping_criteria:
                for initial_state in initial_QAP_states:
                    t = process_time()
                    init_state, solution, score, init_temp, stages, moves, p_cooling = QAP.solve_qap(
                                                                                        init_state=initial_state,
                                                                                        stop_crit_dict=stop_criterion)
                    elapsed_time = process_time() - t
                
            

    except SyntaxError:
        print("Please upgrade your Python installation to a Python 3 version. Aborting..\n")
        return

if __name__ == "__main__":
    main_menu()