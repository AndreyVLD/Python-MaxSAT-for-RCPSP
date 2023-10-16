from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from DataParser import TaskDataParser

# Reading the input RCPSP file
# file_path = input("Please input the file path of the data file: ")
parser = TaskDataParser("Data/Q3_1.dzn")
parser.read_data_from_file()
parser.print_data()

# (Activity, Time) to literal mapping
activity_time_mapping = {}
T = sum(parser.d) + max(parser.d) + 1  # Time horizon
literal_counter = 1

for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    for t in range(0, T - di + 1):
        activity_time_mapping[(i, t)] = literal_counter
        literal_counter += 1

# Creating the corresponding WCNF formula
wcnf = WCNF()

for i in range(1, parser.N_TASKS + 1):
    di = parser.d[i - 1]
    clause = []
    for t in range(0, T - di + 1):
        xi_t = activity_time_mapping[(i, t)]
        clause.append(xi_t)
    wcnf.append(clause)

# Printing to file as DIMACS
wcnf.to_file("Data/Q3_1.wcnf")  # file_path.replace(".dzn", ".wcnf"))
# Reads the formula from a file
# cnf = WCNF(from_file='Data/test1.wcnf')

# Print the soft and hard clauses
# print("Soft: " + cnf.soft.__str__() + "\n" + "Hard: " + cnf.hard.__str__())

# Solve the formula
# rc2 = RC2(cnf)

# Print the solution and the cost
# print(rc2.compute().__str__() + "\n"+rc2.cost.__str__())
