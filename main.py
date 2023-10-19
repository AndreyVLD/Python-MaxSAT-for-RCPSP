from pysat.examples.rc2 import RC2
from pysat.formula import WCNF, CNF
from DataParser import TaskDataParser
from pysat.card import CardEnc
from pysat.pb import *

# Reading the input RCPSP file
# file_path = input("Please input the file path of the data file: ")
parser = TaskDataParser("Data/Q3_1.dzn")
parser.read_data_from_file()
parser.print_data()


activity_time_mapping = {}    # (Activity, Time) started at Time
during_activity = {}    # (Activity, DuringTime) is on during DuringTime
T = sum(parser.d) + max(parser.d) + 1   # Time horizon
literal_counter = 1    # Counter for the literals in the WCNF formula

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

# Creating the corresponding WCNF formula
wcnf = WCNF()

# Completion Clauses S_i
for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    clause = []
    for t in range(0, T - di + 1):
        xi_t = activity_time_mapping[(i, t)]
        clause.append(xi_t)
    wcnf.append(clause)

# Completion Clauses F_i
for t in range(T):
    literals_sum = [activity_time_mapping[(i, t)] for i in range(1, parser.N_TASKS + 1) if
                    (i, t) in activity_time_mapping]
    literals_sum_clause = CardEnc.equals(lits=literals_sum, bound=1,top_id=literal_counter)

    #print(literals_sum)
    #print(literals_sum_clause.clauses)

    highest_variable = max(abs(lit) for clause in literals_sum_clause for lit in clause)
    literal_counter=highest_variable

    #print(highest_variable)

    wcnf.extend(literals_sum_clause)

# Resource Clause C_i
#print(during_activity)

for i in range(1,parser.N_TASKS+1):
    di = parser.d[i-1]
    for t in range(0,T-di+1):
        for u in range(t,t+di-1):
            wcnf.append([-activity_time_mapping[(i,t)],during_activity[(i,u)]])

# Resource Clause R_kt
for t in range(0,T):
    lit_R = [during_activity[(i, t)] for i in range(1, parser.N_TASKS + 1) if
                    (i, t) in during_activity]

    wcnf_r = PBEnc.atmost(lit_R,parser.rr,bound=parser.CAPACITY,top_id=literal_counter)
    # print(lit_R)
    # print(literal_counter)
    # print(wcnf_r.clauses)
    # print()
    wcnf.extend(wcnf_r.clauses)
    highest_variable = max(abs(lit) for clause in wcnf_r for lit in clause)

    literal_counter = highest_variable



# Precedence Clause P_ij
for j in range(parser.N_TASKS):
    dependents = parser.suc[j]
    dj  = parser.d[j]
    z_i_t = []
    if len(dependents) > 0:
        for t in range(0,T-dj+1):
            for i in dependents:
                di = parser.d[i-1]
                for u in  range(0,t-di):
                    z_i_t.append(activity_time_mapping[(i,u)])
                z_i_t.append(-activity_time_mapping[(j+1,t)])
                wcnf.append(z_i_t)
                z_i_t = []

# TODO Weak Clause: what is y_n+1_t ?

# Printing to file as DIMACS
wcnf.to_file("Data/Q3_1.wcnf")  # file_path.replace(".dzn", ".wcnf"))

# Solve the formula
rc2 = RC2(wcnf)

