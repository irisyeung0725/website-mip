#!/usr/bin/python

# This example formulates and solves the following QCP model:
#     minimize    0.04*r + 0.01*o + 0.07*c
#     subject to  r + o + c == 100
#                 c >= 50
#                 r >= 25
#                 r <= 60
#                 Tensile Strength: 0.001 o^2 + 0.10o <= 0.5
#                 Elasticity Constraint: 0.002o^2 - 0.35r + 0.04o <= 1
#                 Hardness Constraint: 0.002r^2 + 0.005o^2 + 0.001c^2 + 0.001r*o + 0.10r + 0.06o - 0.3c <= 1

from gurobipy import *
# print(sys.version)

# Create a new model
m = Model("qcp")

# Create variables
r = m.addVar(name="r")
o = m.addVar(name="o")
c = m.addVar(name="c")

# Set objective: 0.04*r + 0.01*o + 0.07*c
obj = 0.04*r + 0.01*o + 0.07*c

m.setObjective(obj, GRB.MINIMIZE)

# Add all linear constraints: r + o + c == 100, c >= 50, r >= 25, r <= 60
m.addConstr(r + o + c == 100, "c0")
m.addConstr(c >= 50, "c1")
m.addConstr(r >= 25, "c2")
m.addConstr(r <= 60, "c3")

# Add tensile strength constraint: 0.001 o^2 + 0.10o <= 0.5
m.addConstr(0.001*o*o + 0.10*o <= 0.5, "qc0")

# Add elasticity constraint: 0.002o^2 - 0.35r + 0.04o <= 1
m.addConstr(0.002*o*o - 0.35*r + 0.04*o <= 1, "qc1")

# Add hardness constraint: 0.002r^2 + 0.005o^2 + 0.001c^2 + 0.001r*o + 0.10r + 0.06o - 0.3c <= 1
m.addConstr(0.002*r*r + 0.005*o*o + 0.001*c*c + 0.001*r*o + 0.10*r + 0.06*o - 0.3*c <= 1, "qc2")
m.optimize()
m.write("firerock.lp")

for v in m.getVars():
    # print(v)
    print('%s %.2f' % (v.varName, v.x)) # rounded to 2 decimals

org_obj_func = m.getObjective()
opt_val = org_obj_func.getValue()
print('org_obj_func:', org_obj_func)
print("opt_val", org_obj_func.getValue())
opt_var = m.getVars()
number_of_vars = m.NumVars
org_model_sense = m.modelSense
print("opt_var:", opt_var)
print("number_of_vars",number_of_vars)
print("org_model_sense",org_model_sense)
print(opt_var[0].getAttr("Obj"))
print(opt_var[1].getAttr("Obj"))
print(opt_var[2].getAttr("Obj"))
X = {}
l = 2
print ('number_of_vars', number_of_vars)
for i in range(number_of_vars):
    X[l,i] = opt_var[i].X 
print(X)
# # print(opt_var[0].X)
# print(X)
# print(opt_var[0])
# print(m.objVal)
# print(m.getCoeff(0))