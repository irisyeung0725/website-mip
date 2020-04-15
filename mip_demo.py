#!/usr/bin/env python3

from mip import *
input_file_path = "/Users/cassie/Dropbox/GA/Website/p0033.lp"
input_file = input_file_path.split("/")[-1]
output_file_path = "/Users/cassie/Dropbox/GA/Website"
output_file = input_file.split(".")[0]
print(input_file.split('.')[-1] == "lp")
# if (input_file.split('.')[-1])!="lp" or (input_file_name.split('.')[-1])!="mps":
#     f = open ("{0}/{1}_sunny.out".format(output_file_path,output_file_name), 'w')
#     f.write ("Local date and time is: {0} \n\n".format (current_time))
#     f.write("Input file format is incorrect. only .lp/.mps formats are acceptable.")
#     f.close()
#     quit()
# k = int(input("Input k:")) # get value of k
# m = Model(solver_name=CBC) # use cbc solver
# m.read(input_file) # read input file
# m.optimize()
# for v in m.vars:
#     print(v.name,v.x)
# opt_val = m.objective_value
# number_of_vars = len(m.vars)
# org_model_sense = m.sense
# org_obj_func_coeffs = {}
# for i in range(number_of_vars):
#     org_obj_func_coeffs[i]=m.vars[i].obj
# # print(org_obj_func_coeffs)
# if org_model_sense == "MAX":
#     direction = "MAXIMIZATION"
# else:
#     direction = "MINIMIZATION"
# m.sense = "MAX"
# l=0
# X = {}
# for i in range(number_of_vars):
#     X[l,i] = m.vars[i].x
# print(m.objective_value) #3089

# X_k = {}
# c = {}
# s = {}
# q = {}
# epsilon = 1e-6

# Dx_func = LinExpr()

# if org_model_sense == "MAX":
#     for i in range(number_of_vars):
#         Dx_func.add_term(m.vars[i],coeff=-1*org_obj_func_coeffs[i])
#     Dx_func_const = opt_val
# else:
#     for i in range(number_of_vars):
#         Dx_func.add_term(m.vars[i],org_obj_func_coeffs[i])
#     Dx_func_const = -1*opt_val
# Dx_func.add_const(Dx_func_const) # add constant

# # print(Dx_func)
# m.objective = maximize(Dx_func)
# # print(m.objective)
# m.optimize()
# # for i in range(number_of_vars):
# #     print(m.vars[i].name, m.vars[i].x,m.vars[i].var_type)
# # m.optimize()
# MaxDx = m.objective_value # = 2110, sense = MAX, var_type = B
# # ===================================checkmark==============================================#
# new_constr = LinExpr()
# new_constr_const = 0
# for i in range(number_of_vars):
#     if (m.vars[i].var_type == "B") or (m.vars[i].var_type == "I"):
#         if X[l,i] == 0:
#             new_constr.add_term(m.vars[i],coeff=1)
#         else:
#             new_constr.add_term(m.vars[i],coeff=-1)
#             new_constr_const = new_constr_const+1
# new_constr.add_const(new_constr_const) #new_constr = - x + y - z + 2.0
# m.add_constr(new_constr>=1)   #constr(2) = -1.0 x +1.0 y -1.0 z >= -1.0
# l+=1
# for i in range(number_of_vars):
#     c[i] = 0
# for i in range(number_of_vars):
#     if m.vars[i].var_type =="B" or m.vars[i].var_type =="I":
#         for j in range(l):
#             c[i] += X[j,i]
#     c[i] = c[i]/l # c = {0: 1.0, 1: 0.0, 2: 1.0} l=1
# print(c)
# # {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 1.0, 7: 1.0, 8: 0.0, 9: 1.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 1.0, 14: 0.0, 15: 0.0, 16: 0.0, 17: 0.0, 18: 1.0, 19: 1.0, 20: 0.0, 21: 1.0, 22: 0.0, 23: 1.0, 24: 1.0, 25: 1.0, 26: 1.0, 27: 1.0, 28: 1.0, 29: 1.0, 30: 0.0, 31: 0.0, 32: 0.0}
# Nx_func_const = 0
# Nx_func = LinExpr()
# for i in range(number_of_vars):
#     if(m.vars[i].var_type == "B" or m.vars[i].var_type == "I"):
#         Nx_func.add_term(m.vars[i],coeff=1-2*c[i])
#         Nx_func_const += c[i]
#     else:
#         Nx_func.add_term(m.vars[i],coeff=0)
# Nx_func.add_const(Nx_func_const)
# m.objective = maximize(Nx_func)
# m.optimize()
# # status = m.optimize()
# MaxNx = m.objective_value # MaxNx = 19.0
# F = MaxDx / (MaxNx) # F = 111.15789473684211
# for i in range(number_of_vars):
#     X_k[i] = X[l-1,i]  # X_k = {0: 1, 1: 0, 2: 1}
# Nx_value = Nx_func_const #15
# for i in range(number_of_vars):
#     s[i] = (Nx_func.expr[m.vars[i]]) * (X_k[i])
#     Nx_value += s[i] #Nx_value = 0
# Dx_value = Dx_func_const 
# for i in range(number_of_vars):
#     q[i] = (Dx_func.expr[m.vars[i]]) * (X_k[i])
#     Dx_value += q[i] #Dx_value = 0
# Lambda = F * (Nx_value / (Dx_value + epsilon)) #Lambda = 0
# # # # print(Dx_value + epsilon, Nx_value, Lambda)
# # # # DinkleBach_func_const = 1.333332888889037
# DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon))
# print(DinkleBach_func_const) #Lambda=1667.3684210526317
# # # print(DinkleBach_func_const)
# objective = m.objective
# objective.add_const(-1*(objective.const)+DinkleBach_func_const)
# m.objective = objective #objective function = - x + y - z + 1.333332888889037
# for i in range(number_of_vars):
#     coef = (F * Nx_func.expr[m.vars[i]]) - (Lambda * Dx_func.expr[m.vars[i]])
#     m.vars[i].obj = coef #objective function - 0.6666664444445185x + 0.6666664444445185y - 0.6666664444445185z + 1.333332888889037
# m.write('mip-p0033.lp')
# # m.read("gurobi-p0033.lp")
# m.optimize() 
# print("------------------")
# print(m.objective)
# print(m.objective_value)#objective value = 2112.0
# print(m.objective_const) #1667.3684210526317
# print(m.sense) #sensen = Max
# for v in m.vars:
#     print(v.name, v.x)
# # print(m.objective)
# # print("MaxNx",MaxNx)
# # print("MaxDx:",MaxDx, "<Dx_func>",Dx_func,m.sense)
# # print(new_constr) #same as the lp file
# # # print(m.constrs[-1].expr)
# # # print(X)
# for i in range(number_of_vars):
#     X_k[i] = m.vars[i].x
# # #*****************************************************************************
# Nx_value = Nx_func_const #15
# # print(X_k)
# # {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 1, 11: 0, 12: 0, 13: 0, 14: 0, 15: 1, 16: 1, 17: 1, 18: 0, 19: 0, 20: 1, 21: 0, 22: 1, 23: 0, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 0, 30: 1, 31: 1, 32: 1}
# for i in range(number_of_vars):
#     s[i] = (Nx_func.expr[m.vars[i]]) * (X_k[i])
#     Nx_value += s[i] #Nx_value = 19
# Dx_value = Dx_func_const  #-3089
# print(Dx_func.expr[m.vars[0]])
# print(Dx_func)
# for i in range(number_of_vars):
#     q[i] = (Dx_func.expr[m.vars[i]]) * (X_k[i])
#     # print("Q[i]",q[i])
#     Dx_value += q[i] #Dx_value = 1247.0
# print(Dx_value)
# Lambda = F * (Nx_value / (Dx_value + epsilon)) #Lambda = 1.6936647941510306
# print(Lambda)
# print(Dx_func)
# # # # print(Dx_value + epsilon, Nx_value, Lambda)
# # # # DinkleBach_func_const = 1.333332888889037
# # DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon))
# # # print(DinkleBach_func_const)
# # objective = m.objective
# # objective.add_const(-1*(objective.const)+DinkleBach_func_const)
# # m.objective = objective #objective function = - x + y - z + 1.333332888889037
# # for i in range(number_of_vars):
# #     coef = (F * Nx_func.expr[m.vars[i]]) - (Lambda * Dx_func.expr[m.vars[i]])
# #     m.vars[i].obj = coef #objective function - 0.6666664444445185x + 0.6666664444445185y - 0.6666664444445185z + 1.333332888889037
# # m.optimize()
# # print(m.objective_value) #objective value = 1657.2064305940594
# # for i in range(number_of_vars):
# #     X_k[i] = m.vars[i].x 
# # print(X_k)
# # #*****************************************************************************
# # Nx_value = Nx_func_const
# # # print(Nx_value) #Nx_value=15
# # # # print(Nx_value)
# # for i in range(number_of_vars):
# #     s[i] = (Nx_func.expr[m.vars[i]]) * (X_k[i])
# #     Nx_value += s[i] #Nx_value = 15
# # # print(Nx_value)
# # Dx_value = Dx_func_const 
# # # print(Dx_value)
# # for i in range(number_of_vars):
# #     q[i] = (Dx_func.expr[m.vars[i]]) * (X_k[i])
# #     Dx_value += q[i] #Dx_value = 6
# # # print(Dx_value)
# # Lambda = F * (Nx_value / (Dx_value + epsilon)) #Lambda = 277.89469052632353
# # # print(Lambda)
# # print(m.objective_const)
# # # # # print(Dx_value + epsilon, Nx_value, Lambda)
# # # # # DinkleBach_func_const = 1.333332888889037
# # # DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon))
# # # # print(DinkleBach_func_const)
# # # objective = m.objective
# # # objective.add_const(-1*(objective.const)+DinkleBach_func_const)
# # # m.objective = objective #objective function = - x + y - z + 1.333332888889037
# # # for i in range(number_of_vars):
# # #     coef = (F * Nx_func.expr[m.vars[i]]) - (Lambda * Dx_func.expr[m.vars[i]])
# # #     m.vars[i].obj = coef #objective function - 0.6666664444445185x + 0.6666664444445185y - 0.6666664444445185z + 1.333332888889037
# # # m.optimize()
# # # print(m.objective_value) #objective value = 1657.2064305940594
# # # for i in range(number_of_vars):
# # #     X_k[i] = m.vars[i].x 
