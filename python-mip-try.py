#!/usr/bin/env python3

from mip import *

l=0
X={}
X_k={}
c={}
s={}
q={}
epsilon=1e-6


m = Model(solver_name=CBC)
m.read("air03.mps")
m.optimize()
print(m.objective_value) #340160.0
print(m.sense)
m.sense = "MAX"
m.optimize()
# print(m.objective_value) #1471922.0
opt_val = m.objective_value # get objective value
number_of_vars = len(m.vars) # get number of vars
org_model_sense = m.sense # get objective sense
org_obj_func_coeffs = {} # get coefficients for each variable from the objective function
for i in range(number_of_vars):
    org_obj_func_coeffs[i]=m.vars[i].obj
for i in range(number_of_vars):
    X[l,i] = m.vars[i].x
print(X)
# for v in m.vars:
#     print(v.name, v.x)

