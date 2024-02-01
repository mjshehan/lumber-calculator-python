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

    for i in lumber_permutes:
        if sum(i) >= total_linear and sum(i) < total_linear * 1.5:
            test_boards.append(i)

    return test_boards

def input_cut_pieces(): #for testing
    return [45, 45, 45, 45, 66, 66, 66, 66, 66, 66, 66, 66, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 12, 11, 55, 29, 50, 49]

def create_data_model(cut_pieces, lumber_sizes):
    data = {}
    data["weights"] = cut_pieces
    data["values"] = len(data["weights"]) * [1]
    assert len(data["weights"]) == len(data["values"])
    data["num_items"] = len(data["weights"])
    data["all_items"] = range(data["num_items"])
    data["bin_capacities"] = lumber_sizes
    data["num_bins"] = len(data["bin_capacities"])
    data["all_bins"] = range(data["num_bins"])
    return data

#create the MIP solver     
def create_solver():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        print("SCIP solver unavailable.")
        return solver
    return solver

#solver the MIP problem
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

    # Objective: Maximize total value of packed items.
    objective = solver.Objective()
    for i in data["all_items"]:
        for b in data["all_bins"]:
            objective.SetCoefficient(x[i, b], data["values"][i])
    objective.SetMaximization()

    #print(f"Solving with {solver.SolverVersion()}") #print the solver version
    status = solver.Solve()
    if status is not pywraplp.Solver.OPTIMAL:
        return None
    if status == pywraplp.Solver.OPTIMAL:
        total_weight = 0
        total_value = 0
        df = pd.DataFrame(columns=['bin', 'capacity', 'cut'])

        for b in data["all_bins"]:
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if x[i, b].solution_value() > 0:
                    new_df = pd.DataFrame(columns=['bin', 'capacity', 'cut'])
                    new_df.loc[0] = [b, data['bin_capacities'][b], data["weights"][i]]
                    df = pd.concat([df, new_df], ignore_index=True)
                    bin_weight += data["weights"][i]
                    bin_value += data["values"][i]
            total_weight += bin_weight
            total_value += bin_value

        #create a new dataframe to group results for output
        grouped_df = df.groupby('bin').agg(
            {'capacity': 'first',  # get the first capacity value in each group
             'cut': ['sum', list]  # sum the cut values in each group
            }).reset_index()
        grouped_df.columns = grouped_df.columns.get_level_values(0)
        grouped_df.columns.values[0] = 'bin'
        grouped_df.columns.values[0] = 'bin'
        grouped_df.columns.values[1] = 'lumber length'
        grouped_df.columns.values[2] = 'inches used'
        grouped_df.columns.values[3] = 'cuts'
        grouped_df['waste'] = grouped_df['lumber length'] - grouped_df['inches used']
        
        #Return the grouped dataframe if we have packed all the items i.e. all cuts are accounted for
        if total_value == len(data["weights"]):    
            return grouped_df
        else: 
            return None
    else:
        print("The problem does not have an optimal solution.")


#calculator function to call the solver
def calculate(lumber, cut_pieces):
    start_time = time.time() 
    test_boards = permute_lumber_sizes(lumber, cut_pieces)
    found_solution = None

    permute_count = 0

    #Iterate over possible lumber combinations, calling solver on each one
    for board_permute in test_boards:
        permute_count += 1
        print("permute count: ", permute_count, "/", len(test_boards))
        iter_time = time.time()
        solver = create_solver()
        solver.SetTimeLimit(3000)
        data = create_data_model(cut_pieces, board_permute)
        found_solution = optimize(data, solver)

        #Continue to the next iteration if no solution is found
        if found_solution is None:
            continue                 
        #Break if a solution is found and all cuts are accounted for
        if found_solution is not None and sum(sum(sublist) for sublist in found_solution['cuts']) == sum(cut_pieces):   
            break

    print("SOLUTION FOUND on permute #: ", permute_count)
    print("total elapsed time..........", time.time()-start_time)
    print("Time for final iteration...." , time.time() - iter_time)
    print("total cut pieces: " , len(cut_pieces))
    print("number of raw boards: ", len(found_solution))
    return found_solution

#Main program for testing
def main():

    lumber = [] #enter values for testing    
    cut_pieces = [[]] #enter values for testing
    test_boards = permute_lumber_sizes(lumber)

    found_solution = None

    for board_permute in test_boards:
        if found_solution is None:
            data = create_data_model(cut_pieces, board_permute)
            solver = create_solver()
            found_solution = optimize(data, solver)
        else:
            break
    
    print(found_solution)

if __name__ == "__main__":
    main()