"""Solve a multiple knapsack problem using a MIP solver."""
from ortools.linear_solver import pywraplp

def input_board_sizes():
    #return [int(input("What is the length of the first size of lumber: ")), int(input("What is the length of the second size of lumber: ")), int(input("What is the length of the third size of lumber: "))] 
    return 8 * [144] + [72] + [96]

def create_data_model(lumber_sizes):
    data = {}
    data["weights"] = [45, 45, 45, 45, 66, 66, 66, 66, 66, 66, 66, 66, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 12, 11, 55, 29, 50, 49]
    print("total linear feet: ", sum(data["weights"]))
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

    if status == pywraplp.Solver.OPTIMAL:
        print(f"Total packed value: {objective.Value()}")
        total_weight = 0
        total_value = 0
        for b in data["all_bins"]:
            print(f"Bin {b}")
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]} value: {data['values'][i]}"
                    )
                    bin_weight += data["weights"][i]
                    bin_value += data["values"][i]
            print(f"Packed bin weight: {bin_weight}")
            print(f"Packed bin value: {bin_value}\n")
            total_weight += bin_weight
            total_value += bin_value
        print(f"Total packed weight: {total_weight}")
        print(f"Total value: {total_value}")
    else:
        print("The problem does not have an optimal solution.")

def main():
    
    lumber = input_board_sizes()  

    data = create_data_model(lumber)
    solver = create_solver()
    optimize(data, solver)
    
    # Variables.
    # x[i, b] = 1 if item i is packed in bin b.
    


if __name__ == "__main__":
    main()