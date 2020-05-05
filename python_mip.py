#!/usr/bin/env python3

from mip import *

# from mip import Model, xsum, maximize, BINARY
## --------------------------------------------------------------- ##
# example the 0/1 Knapsack Problem
# p = [10, 13, 18, 31, 7, 15]
# w = [11, 15, 20, 35, 10, 33]
# c, I = 47, range(len(w))

# m = Model("Knapsack", sense=MAXIMIZE, solver_name=CBC)
# x = [m.add_var(var_type=BINARY) for i in I]
# m.objective = maximize(xsum(p[i] * x[i] for i in I))
# m += xsum(w[i] * x[i] for i in I) <= c

# m.write('mip_example.lp')
# m.optimize()


# selected = [i for i in I if x[i].x >= 0.99]
# print('selected items: {} '.format(selected))

## --------------------------------------------------------------- ##
# build my own example "MIP1"
m = Model("python_mip1",sense=MINIMIZE,solver_name=CBC)

x = m.add_var("x",var_type=BINARY)
y = m.add_var("y",var_type=BINARY)
z = m.add_var("z",var_type=BINARY)

m.objective = x + y + 2*z
m.add_constr(x + 2 * y + 3 * z <= 4 ,"c0")
m.add_constr(x + y >= 1 ,"c1")
m.write("mip_mip1_minimize.lp")
m.optimize()
print('model has {} vars, {} constraints and {} nzs'.format(m.num_cols, m.num_rows, m.num_nz))
print(m.objective_value)
for v in m.vars:
    # if abs(v.x) > 1e-6: # only printing non-zeros
    print('{} : {}'.format(v.name, v.x))
# print(m.sense)
## --------------------------------------------------------------- ##
# read an imported .lp model
# m = Model(solver_name=CBC)
# m.read("mip_mip1.lp")
# m.optimize()
# print("Objective value:", int(-1*(m.objective_value))) # objective value
# for v in m.vars:
#     # if abs(v.x) > 1e-6: # only printing non-zeros
#     print('{} : {} : {}'.format(v.name, v.x, v.obj)) # name, value, coefficient
# print("get model sense:", m.sense, "| get status:", m.status == OptimizationStatus.OPTIMAL)
# for v in m.vars:
#     print(v.name,v.var_type)
# print("number_of_vars", len(m.vars)) # get the number of vars
# # for v in m.constrs:
# #     print(v.name,v.rhs,v.expr)
# # print(m.vars[0], m.vars[0].column)
# # print(m.vars[1], m.vars[1].column)
# # print(m.objective)
# # print("model sense",m.sense)
# X = {}
# l = 0
# for i in range(len(m.vars)):
#     X[l,i] = m.vars[i].x
# print(X)
## --------------------------------------------------------------- ##
# import os
# from datetime import datetime
# input_file_path = "/Users/cassie/Dropbox/GA/Website/mip_mip1.lp"
# input_file = "mip_mip1.lp"
# output_file_path = "/Users/cassie/Dropbox/GA/Website"
# output_file = input_file.split(".")[0]
# # k = input("Input k:")
# m = Model(solver_name=CBC)
# m.read(input_file)
# # m.objective.add_const(3)

# m.optimize()
# for v in m.vars:
# #     # if abs(v.x) > 1e-6: # only printing non-zeros
#     print('{} : {}'.format(v.name, v.x))

# print(m.objective_value)
# print(len(m.vars))
# opt_val = m.objective_value
# number_of_vars = len(m.vars)
# org_model_sense = m.sense
# org_obj_func_coeffs = {}
# for i in range(number_of_vars):
#     org_obj_func_coeffs[i]=m.vars[i].obj
# if org_model_sense == "MAX":
#     direction = "MAXIMIZATION"
# else:
#     direction = "MINIMIZATION"
# m.sense = "MAX"
# l=2
# X = {}
# for i in range(number_of_vars):
#     X[l,i] = m.vars[i].x


# # f = open("{0}/{1}.txt".format(output_file_path,output_file), 'w')
# # f.write("Local date and time is: {0} \n\n".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
# # f.write("Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file))
# # f.write ( "Original objective function direction is {0}\n".format(direction))
# # f.write ("Diversity metric is to maximize distance from centroid\n\n")
# # f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
# # f.write ("N/A          N/A        %10.5f         0                  0              " %(opt_val))
# # for i in range(number_of_vars):
# # 			f.write("%.0f" %abs(X[l,i])) 
# # f.write ("\n")
# print(m.sense)
# # now = datetime.now()
 
# # print("now =", now)
# # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# # print("date and time =", dt_string)	

# # Dx_func = LinExpr()
# # Dx_func.add_const(2)
# # Dx_func.add_var(a,1)
# a = m.add_var("a",var_type=BINARY)
# # Dx_func.add_var(a,2)
# # m.add_constr(Dx_func<=1)
# # print(m.constrs[2].expr)
# # Dx_func.add_term(m.vars[0],2)
# # print(Dx_func)
# print(m.vars[0].var_type == "I")
# print(m.constrs[0].expr.expr[m.vars[0]])
# print(type(m.constrs[0].expr))
# # print(type(Dx_func))
# # Dx_func.add_const(5.0)
# # print(Dx_func)
# # m.objective.add_const(-3)
# print(type(m.objective))
# print(m.objective)

# # m -= 5
# # m.objective.add_const(-5)

# obj = m.objective

# obj.add_const(5)
# print(obj)

# m.objective = obj
# print("--------")
# print(obj)
# m.vars[0].obj = 2
# # m.optimize()
# print("--------------")
# print(m.vars[0].obj)
# print(m.objective)
# print("----")
# print("aaaa", obj)

# print(s)
# print(type(m.objective))
# print("m.obj:", m.objective)
# print(m.objective_value)
# Dx_func.add_const(4)
# print(Dx_func)
# print(m.optimize())

# f = open("/Users/cassie/Dropbox/GA/Website/mknap_4.lp",'r')
# output = open("/Users/cassie/Dropbox/GA/Website/mknap_4_new.lp",'w+')
# for line in f:
#     if "obj:" in line:
#         # print(line)
#         line = line.replace("obj:", " ")
#     output.write(line)
# # f.close()
#     # f.write(line)
# print(output.read())
import os
import sys
import fileinput

for line in fileinput.input('/Users/cassie/Dropbox/GA/Website/mknap_4.lp', inplace=1):
        sys.stdout.write(line.replace('obj:', ' '))
# a = "happy day"
# a = a.replace("happy",'')
# print(a)
