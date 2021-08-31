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
            initial_QAP_states = set_init_QAP_states()
            initial_CMLBK_states = set_init_CMLBK_states()
            QAP = qap.QAP(is_debug=False)
            CMLBK = cmlbk.CMLBK(is_debug=False)

            # for item in initial_QAP_states:
            #     QAP.solve_qap(item)
            
            for item in initial_CMLBK_states:
                CMLBK.solve_cmlbk(item)

            

    except SyntaxError:
        print("Please upgrade your Python installation to a Python 3 version. Aborting..\n")
        return

if __name__ == "__main__":
    main_menu()