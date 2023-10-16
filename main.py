from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from DataParser import TaskDataParser

# Reads the formula from a file
parser = TaskDataParser("Data/Q3_1.dzn")
parser.read_data_from_file()
parser.print_data()
#cnf = WCNF(from_file='Data/test1.wcnf')

# Print the soft and hard clauses
#print("Soft: "+cnf.soft.__str__()+"\n"+"Hard: "+cnf.hard.__str__())

# Solve the formula
#rc2 = RC2(cnf)

# Print the solution and the cost
#print(rc2.compute().__str__() + "\n"+rc2.cost.__str__())



