from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from DataParser import TaskDataParser

# Reading the input RCPSP file
file_path = input("Please input the file path of the data file: ")
parser = TaskDataParser(file_path)
parser.read_data_from_file()
parser.print_data()

# Creating the corresponding WCNF formula
cnf = WCNF()

# Printing to file as DIMACS
cnf.to_file(file_path.replace(".dzn", ".wcnf"))





# Reads the formula from a file
# cnf = WCNF(from_file='Data/test1.wcnf')

# Print the soft and hard clauses
# print("Soft: "+cnf.soft.__str__()+"\n"+"Hard: "+cnf.hard.__str__())

# Solve the formula
# rc2 = RC2(cnf)

# Print the solution and the cost
# print(rc2.compute().__str__() + "\n"+rc2.cost.__str__())
