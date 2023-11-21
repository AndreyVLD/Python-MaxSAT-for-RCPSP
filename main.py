from pysat.examples.rc2 import RC2
from pysat.formula import WCNF, CNF
from DataParser import TaskDataParser
from pysat.card import CardEnc
from pysat.pb import *

# Parser data structure info:
# CAPACITY = maximum resource capacity
# N_TASKS = number of tasks
# d = list of durations of each task
# rr = list of resource requirements of each task
# suc = list of successors of each task ( list of lists )


# Reading the input RCPSP file
file_path = input("Please input the file path of the data file: ")
parser = TaskDataParser(file_path)
parser.read_data_from_file()
parser.print_data()

activity_time_mapping = {}  # (Activity, Time) started at Time
during_activity = {}  # (Activity, DuringTime) is on during DuringTime
T = sum(parser.d) + max(parser.d) + 1  # Time horizon
literal_counter = 1  # Counter for the literals in the WCNF formula

# (Activity, Time) to literal mapping
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    for t in range(0, T - di + 1):
        activity_time_mapping[(i, t)] = literal_counter
        literal_counter += 1

# (Activity, DuringTime) to literal Mapping
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    for t in range(0, T):
        during_activity[(i, t)] = literal_counter
        literal_counter += 1

dummy_task = parser.N_TASKS + 1
for t in range(0, T):
    activity_time_mapping[(dummy_task, t)] = literal_counter
    literal_counter += 1
# Creating the corresponding WCNF formula
wcnf = WCNF()

# Adding the dummy task
for t in range(0, T):
    wcnf.append([-activity_time_mapping[(dummy_task, t)]], weight=t + 1)

# Completion Clauses S_i
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    clause = []
    for t in range(0, T - di + 1):
        xi_t = activity_time_mapping[(i, t)]
        clause.append(xi_t)
    wcnf.append(clause)

# Completion Clauses for dummy task
literals = []
for t in range(0, T):
    literals.append(activity_time_mapping[(dummy_task, t)])
clause = CardEnc.equals(lits=literals, bound=1, top_id=literal_counter)
wcnf.extend(clause)

# Calculating the highest variable to avoid collisions from the auxiliary variables
highest_variable = max(abs(lit) for clause in clause for lit in clause)
literal_counter = highest_variable

# Completion Clauses F_i
for t in range(T):
    literals_sum = [activity_time_mapping[(i, t)] for i in range(1, parser.N_TASKS + 1) if
                    (i, t) in activity_time_mapping]
    literals_sum_clause = CardEnc.equals(lits=literals_sum, bound=1, top_id=literal_counter)

    # Calculating the highest variable to avoid collisions from the auxiliary variables
    highest_variable = max(abs(lit) for clause in literals_sum_clause for lit in clause)
    literal_counter = highest_variable

    wcnf.extend(literals_sum_clause)

# Resource Clause C_i
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    for t in range(0, T - di + 1):
        for u in range(t, t + di - 1):
            wcnf.append([-activity_time_mapping[(i, t)], during_activity[(i, u)]])

# Resource Clause R_k_t
for t in range(0, T):
    lit_R = [during_activity[(i, t)] for i in range(1, parser.N_TASKS + 1) if
             (i, t) in during_activity]

    wcnf_r = PBEnc.atmost(lit_R, parser.rr, bound=parser.CAPACITY, top_id=literal_counter)

    wcnf.extend(wcnf_r.clauses)
    highest_variable = max(abs(lit) for clause in wcnf_r for lit in clause)

    literal_counter = highest_variable

# Precedence Clause P_i_j
for j in range(parser.N_TASKS):

    # For every task we get the dependents
    dependents = parser.suc[j]
    dj = parser.d[j]

    # Vector of dependents
    z_i_t = []
    if len(dependents) > 0:  # If there are dependents
        for t in range(0, T - dj + 1):  # For every time step
            for i in dependents:  # For every dependent
                di = parser.d[i - 1]
                for u in range(0, t - di):  # Computing z_i_t
                    z_i_t.append(activity_time_mapping[(i, u)])
                z_i_t.append(-activity_time_mapping[(j + 1, t)])  # Adding -x_j_t
                wcnf.append(z_i_t)  # Appending the clause with AND
                z_i_t = []

# Weak Clause W_i with dummy task
z_i_t = []
for t in range(0, T):  # For every time step
    for i in range(1, parser.N_TASKS + 1):  # For every dependent
        di = parser.d[i - 1]
        for u in range(0, t - di):  # Computing z_i_t
            z_i_t.append(activity_time_mapping[(i, u)])
        z_i_t.append(-activity_time_mapping[(dummy_task, t)])
        wcnf.append(z_i_t)  # Appending the clause with AND
        z_i_t = []

# Printing to file as DIMACS
wcnf.to_file(file_path.replace(".dzn", ".wcnf"))

# Solve the formula
rc2 = RC2(wcnf)
solution = rc2.compute()

print(solution)
# Print the solution
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    for t in range(0, T - di + 1):
        if solution[activity_time_mapping[(i, t)] - 1] >= 0:
            print(f"Task {i} starts at time {t}")
            break
