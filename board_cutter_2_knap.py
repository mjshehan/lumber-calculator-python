"""Solve a multiple knapsack problem using a MIP solver."""
from ortools.linear_solver import pywraplp
import math
from itertools import combinations_with_replacement
from combo_test import *
from collections import namedtuple
import pandas as pd
import time


def input_board_sizes():
    #return [int(input("What is the length of the first size of lumber: ")), int(input("What is the length of the second size of lumber: ")), int(input("What is the length of the third size of lumber: "))] 
    return 8 * [144] + [72] + [96]

def permute_lumber_sizes(lumber, cut_pieces):
    size_1 = lumber[0]
    size_2 = lumber[1]
    size_3 = lumber[2]
    total_linear = sum(cut_pieces)
    lumber_sizes = [size_1, size_2, size_3]
    max =  math.ceil(total_linear * 1.3 / size_1) #find the max number of raw boards to perute
    lumber_permutes = arrange_intervals(lumber_sizes, max)

    test_boards = []

    print("-------------------TOTAL LINEAR---", total_linear )
    for i in lumber_permutes:
        if sum(i) >= total_linear and sum(i) < total_linear * 1.5:
            test_boards.append(i)

    return test_boards

def input_cut_pieces(): #for testing
    return [45, 45, 45, 45, 66, 66, 66, 66, 66, 66, 66, 66, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 12, 11, 55, 29, 50, 49]

def create_data_model(cut_pieces, lumber_sizes):
    print("testing lumber sizes:  ", lumber_sizes)
    print("testing linear inches of raw lumber:  ", sum(lumber_sizes))
    data = {}
    data["weights"] = cut_pieces
    print("total linear feet needed: ", sum(data["weights"]))
    print("total boards needed: ", len(data["weights"]))
    data["values"] = len(data["weights"]) * [1]
    assert len(data["weights"]) == len(data["values"])
    data["num_items"] = len(data["weights"])
    data["all_items"] = range(data["num_items"])

    """figure out the total linear feet of lumber required -- then figure out how many boards of each size are needed... start trying the problem until we pack a value of sum(data["values"]) into the bins])"""

    data["bin_capacities"] = lumber_sizes
    data["num_bins"] = len(data["bin_capacities"])
    data["all_bins"] = range(data["num_bins"])

    # Create the mip solver with the SCIP backend.
    
    return data

def create_solver():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        print("SCIP solver unavailable.")
        return solver
    return solver

def optimize(data, solver):
    x = {}
    for i in data["all_items"]:
        for b in data["all_bins"]:
            x[i, b] = solver.BoolVar(f"x_{i}_{b}")

    # Constraints.
    # Each item is assigned to at most one bin.
    for i in data["all_items"]:
        solver.Add(sum(x[i, b] for b in data["all_bins"]) <= 1)

    # The amount packed in each bin cannot exceed its capacity.
    for b in data["all_bins"]:
        solver.Add(
            sum(x[i, b] * data["weights"][i] for i in data["all_items"])
            <= data["bin_capacities"][b]
        )

    # Objective.
    # Maximize total value of packed items.
    objective = solver.Objective()
    for i in data["all_items"]:
        for b in data["all_bins"]:
            objective.SetCoefficient(x[i, b], data["values"][i])
    objective.SetMaximization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    print("test line")
    if status is not pywraplp.Solver.OPTIMAL:
        print('here we are baby --------------------')
        return None
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Total packed value: {objective.Value()}")
        total_weight = 0
        total_value = 0

        df = pd.DataFrame(columns=['bin', 'capacity', 'cut'])

        cuts = []
       
        for b in data["all_bins"]:
            print(f"Lumber {b} capacity: {data['bin_capacities'][b]}")
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if x[i, b].solution_value() > 0:
                    new_df = pd.DataFrame(columns=['bin', 'capacity', 'cut'])
                    new_df.loc[0] = [b, data['bin_capacities'][b], data["weights"][i]]
                    df = pd.concat([df, new_df], ignore_index=True)
                    bin_weight += data["weights"][i]
                    bin_value += data["values"][i]
            print(f"Packed bin weight: {bin_weight}")
            print(f"Packed bin value: {bin_value}\n")
            total_weight += bin_weight
            total_value += bin_value
        print(f"Total packed weight: {total_weight}")
        print(f"Total value: {total_value}")
        #print("here is the df----------------------->>>>>>>>>>>> ", df)
        
        
        ####################
        grouped_df = df.groupby('bin').agg(
            {'capacity': 'first',  # get the first capacity value in each group
             'cut': ['sum', list]  # sum the cut values in each group
            }).reset_index()

        # calculate the waste for each bin
        #grouped_df['waste'] = grouped_df['capacity'] - grouped_df['cut']
        
        # rename the 'cut' column to 'total_used'
        grouped_df.columns = grouped_df.columns.get_level_values(0)
        grouped_df.columns.values[0] = 'bin'
        grouped_df.columns.values[0] = 'bin'
        grouped_df.columns.values[1] = 'lumber length'
        grouped_df.columns.values[2] = 'inches used'
        grouped_df.columns.values[3] = 'cuts'
        grouped_df['waste'] = grouped_df['lumber length'] - grouped_df['inches used']




        #grouped_df.rename(columns={'capacity': 'BOARD LENGTH', 'sum': 'USED', 'cut': 'CUT LIST'}, inplace=True)
        
        
        
        print("GROUP DF........\n", grouped_df)
        ####################
        print("total value-----------------------> ", total_value)
        print("pieces needed -------------", len(data["weights"]))
        if total_value == len(data["weights"]):
            
            return grouped_df
        else: 
            return None
    else:
        print("The problem does not have an optimal solution.")


def calculate(lumber, cut_pieces):

    start_time = time.time() 
    timeout = 3 

    test_boards = permute_lumber_sizes(lumber, cut_pieces)
    found_solution = None

    permute_count = 0
    for board_permute in test_boards:
        permute_count += 1
        print("permute count: ", permute_count)
        print("total permutes:", len(test_boards))
        #iter_time = time.time()
        solver = create_solver()
        solver.SetTimeLimit(3000)
        data = create_data_model(cut_pieces, board_permute)
        found_solution = optimize(data, solver)
        if found_solution is None:
            continue
        
        #print("sum: ", sum(sum(sublist) for sublist in found_solution['cuts']))
        #print("len: ", len(cut_pieces))
        
        if found_solution is not None and sum(sum(sublist) for sublist in found_solution['cuts']) == sum(cut_pieces):   
            break

    #print("solved -------------------------\n", found_solution)
    #print("ELAPSED TIME------------------", time.time()-start_time)
    #print("Time for iteration...." , time.time() - iter_time)
    return found_solution
def main():
    
    lumber = input_board_sizes()  
    cut_pieces = input_cut_pieces()
    test_boards = permute_lumber_sizes(cut_pieces)

    found_solution = None

    for board_permute in test_boards:
        if found_solution is None:
            data = create_data_model(cut_pieces, board_permute)
            solver = create_solver()
            found_solution = optimize(data, solver)
        else:
            break
    
    print(found_solution)


    # Variables.
    # x[i, b] = 1 if item i is packed in bin b.
    


if __name__ == "__main__":
    main()