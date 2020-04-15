#!/usr/bin/env python3

# Import PuLP modeler functions
from pulp import *
import pulp as pl

# A new LP problem
prob = "test.lp"
prob = LpProblem("test1", LpMaximize)

# Variables
# 0 <= x <= 4
x = LpVariable("x", cat="Binary")
# -1 <= y <= 1
y = LpVariable("y", cat="Binary")
# 0 <= z
z = LpVariable("z", cat="Binary"),
# Use None for +/- Infinity, i.e. z <= 0 -> LpVariable("z", None, 0)

# Objective
prob += x + y + 2 * z, "obj"
# (the name at the end is facultative)

# Constraints
prob += x + 2 * y + 3 * z <= 4, "c1"
prob += x + y >= 1 , "c2"
# prob += r >= 25, "c3"
# prob += r <= 60, "c4"

# (the names at the end are facultative)

# Write the problem as an LP file
prob.writeLP("test1.lp")

# Solve the problem using the default solver
prob.solve(GLPK())
prob.solve()
# pulp.solve(pulp.GLPK_CMD())
# Use prob.solve(GLPK()) instead to choose GLPK as the solver
# Use GLPK(msg = 0) to suppress GLPK messages
# If GLPK is not in your path and you lack the pulpGLPK module,
# replace GLPK() with GLPK("/path/")
# Where /path/ is the path to glpsol (excluding glpsol itself).
# If you want to use CPLEX, use CPLEX() instead of GLPK().
# If you want to use XPRESS, use XPRESS() instead of GLPK().
# If you want to use COIN, use COIN() instead of GLPK(). In this last case,
# two paths may be provided (one to clp, one to cbc).

# Print the status of the solved LP
print("Status:", LpStatus[prob.status])

# Print the value of the variables at the optimum
for v in prob.variables():
	print(v.name, "=", v.varValue)

# Print the value of the objective
print("objective=", value(prob.objective))
print("prob_sense=", prob.getSense())
print("obj=", prob.objective)
print("prob_var=", prob.variables())
# print(type(prob.numVariables()))
# print(type(prob.variables()))
print(value(prob.objective))
# print(prob.variablesDict())
# print(prob.variables()[0].cat)
for var in prob.variables():
    print(var.cat)
# prob.addVariable()
# print(prob.coefficients())