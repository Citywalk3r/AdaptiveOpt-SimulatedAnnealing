from pathlib import Path
import numpy as np
import random
import math




def main_menu():
    print_str = """Welcome to Adaptive Optimization HW_1: Simulated Annealing\n
            The available problems are the following:\n
            1) Combinatorial Optimization -- QAP\n
            2) Continuous Optimization: 6 hump camelback function\n
            """
    print(print_str)
    try:
        selection = input("Please type 1 or 2 and press ENTER...\n")
        while selection!="1" and selection!="2":
            selection = input("Invalid choice. Please type 1 or 2 and press ENTER...\n")
        if selection=="1":
            Qap()
        else:
            Cmlbk()
    
    except SyntaxError:
        print("Please upgrade your Python installation to a Python 3 version. Aborting..\n")
        return
    
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

# TODO
def move(currState):
    nextState = currState
    return nextState

def eval_func(currState):
    """
    Minimization is the objective.
    A lower returned value is better 
    """
    pass


def sim_annealing(x0,t0,m,n,a):
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
            Xtemp = move(X[i])
            if eval_func(Xtemp)<= eval_func(X[i]):
                X[i+1] = Xtemp
            else:
                if random.uniform(0, 1) <= math.exp(-((eval_func(Xtemp)-eval_func(X[i]))/T[t])):
                    X[i+1] = Xtemp
                else:
                    X[i+1] = X[i]
            if eval_func(X[i+1]) <= eval_func(Xf):
                Xf = X[i+1]
        T[t+1] = a*T[t]
    return Xf

def Qap():
    flow, dist = parse_data()

    # DEBUG
    # print(flow.shape)
    # print(flow)
    # print("----------------")
    # print(dist)
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
       
def Cmlbk():
    pass

if __name__ == "__main__":
    main_menu()