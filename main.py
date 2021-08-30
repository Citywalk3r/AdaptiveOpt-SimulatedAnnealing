import qap

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
            QAP = qap.QAP(is_debug=False)
            QAP.solve_qap()
        else:
            pass
    
    except SyntaxError:
        print("Please upgrade your Python installation to a Python 3 version. Aborting..\n")
        return

if __name__ == "__main__":
    main_menu()