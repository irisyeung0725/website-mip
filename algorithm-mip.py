#!/usr/bin/env python3

from mip import *
import sys
import os
from datetime import datetime

## ----------------------------------------------------------------> ##
# check user input
# if len(sys.argv)<3:
#     if len(sys.argv)<2:
#         print('Please Enter Your Lp/MPS File and K')
#     else:
#         print("Please Enter your K")
    # quit()
## ----------------------------------------------------------------> ##
# Handle user input and output
input_file_path = "/Users/cassie/Dropbox/GA/Website/mknap_2.lp"
input_file = input_file_path.split("/")[-1]
output_file_path = "/Users/cassie/Dropbox/GA/Website"
output_file = input_file.split(".")[0]
k = int(input("Input k:")) # get value of k
m = Model(solver_name=CBC)
# model = m
# model.lp_method = 0
# model.read(input_file)
m.read(input_file) # read input file
m.optimize()
# print(m.objective_value)
## ----------------------------------------------------------------> ##
opt_val = m.objective_value
number_of_vars = len(m.vars)
org_model_sense = m.sense
org_obj_func_coeffs = {}
for i in range(number_of_vars):
    org_obj_func_coeffs[i]=m.vars[i].obj
# print(org_obj_func_coeffs)
if org_model_sense == "MAX":
    direction = "MAXIMIZATION"
else:
    direction = "MINIMIZATION"
m.sense = "MAX"
l=0
X = {}
print(number_of_vars)
for i in range(number_of_vars):
    X[l,i] = m.vars[i].x
# # print(X)

f = open("{0}/{1}_test.txt".format(output_file_path,output_file), 'w')
f.write("Local date and time is: {0} \n\n".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
f.write("Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file))
f.write ("Original objective function direction is {0}\n".format(direction))
f.write ("Diversity metric is to maximize distance from centroid\n\n")
f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
f.write ("N/A          N/A        %10.5f         0                  0              " %(opt_val))
for i in range(number_of_vars):
	f.write("%.0f" %abs(X[l,i])) 
f.write ("\n")

## ----------------------------------------------------------------> ##
# start algorithm
X_k = {}
c = {}
s = {}
q = {}
epsilon = 1e-6

Dx_func = LinExpr()

if org_model_sense == "MAX":
    for i in range(number_of_vars):
        Dx_func.add_term(m.vars[i],coeff=-1*org_obj_func_coeffs[i])
    Dx_func_const = opt_val
else:
    for i in range(number_of_vars):
        Dx_func.add_term(m.vars[i],org_obj_func_coeffs[i])
    Dx_func_const = -1*opt_val
Dx_func.add_const(Dx_func_const) # add constant

# print(Dx_func)
m.objective = maximize(Dx_func)
# print(m.objective)
m.optimize()
# for i in range(number_of_vars):
#     print(m.vars[i].name, m.vars[i].x,m.vars[i].var_type)
# m.optimize()
MaxDx = m.objective_value # = 2.0, sense = MAX, var_type = B
# print(Dx_func)
# print(MaxDx)
# print(X)

# ============================================================================ #
while (l<k):
    # Add new constraints
    new_constr = LinExpr()
    new_constr_const = 0
    for i in range(number_of_vars):
        if (m.vars[i].var_type == "B") or (m.vars[i].var_type == "I"):
            if X[l,i] == 0:
                new_constr.add_term(m.vars[i],coeff=1)
            else:
                new_constr.add_term(m.vars[i],coeff=-1)
                new_constr_const = new_constr_const+1
    new_constr.add_const(new_constr_const)
    m.add_constr(new_constr>=1)

    # increase l
    l = l + 1

    # calcualte centroid
    for i in range(number_of_vars):
        c[i] = 0
    for i in range(number_of_vars):
        if m.vars[i].var_type =="B" or m.vars[i].var_type =="I":
            for j in range(l):
                c[i] += X[j,i]
        c[i] = c[i]/l

    # build and solve Max_N(x)
    Nx_func_const = 0
    Nx_func = LinExpr()
    for i in range(number_of_vars):
        if(m.vars[i].var_type == "B" or m.vars[i].var_type == "I"):
            Nx_func.add_term(m.vars[i],coeff=1-2*c[i])
            Nx_func_const += c[i]
        else:
            Nx_func.add_term(m.vars[i],coeff=0)
    Nx_func.add_const(Nx_func_const)
    m.objective = Nx_func
    m.optimize()

    # check and terminate if new model 
    status = m.optimize()
    if status != OptimizationStatus.OPTIMAL:
        f = open("{0}/{1}.out".format(output_file_path,output_file), 'a+')
        f.write("All feasible solutions have been identified. Present model is infeasible.")
        f.close()
        quit()

    # calculate normalization factor f 
    MaxNx = m.objective_value
    F = MaxDx / (MaxNx + epsilon)

    # Identify initial solution x0 to pass into dinkelbach
    for i in range(number_of_vars):
        X_k[i] = X[l-1,i]

    true = 1
    counter = 0

    # start dinkelbach
    while true:
        counter += 1
        # calculate Nx
        Nx_value = Nx_func_const
        for i in range(number_of_vars):
            s[i] = (Nx_func.expr[m.vars[i]]) * (X_k[i])
            Nx_value += s[i]
        # calculate Dx
        Dx_value = Dx_func_const
        for i in range(number_of_vars):
            q[i] = (Dx_func.expr[m.vars[i]]) * (X_k[i])
            Dx_value += q[i]

        # calculate Lambda
        Lambda = F * (Nx_value / (Dx_value + epsilon)) 

        # create F*N(x) - Lambda*D(x)  
        DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon))
        objective = m.objective
        objective.add_const(-1*(objective.const) + DinkleBach_func_const)
        m.objective = objective

        for i in range(number_of_vars):
            coef = (F * Nx_func.expr[m.vars[i]]) - (Lambda * Dx_func.expr[m.vars[i]])
            m.vars[i].obj = coef
        
        m.optimize()

        if (-0.001 <= m.objective_value <= 0.001):
            for i in range(number_of_vars):
                X[l,i] = m.vars[i].x
            f.write ("%3d          %3d        %10.5f      %10.5f         %10.5f        " %(l,counter,abs(opt_val - Dx_value),Dx_value,Nx_value))
            for i in range(number_of_vars):
                f.write("%.0f" %abs(X[l,i])) 
            f.write ("\n")

            true = 0
        else:
            for i in range(number_of_vars):
                X_k[i] = m.vars[i].x

f.close()
                






