#!/usr/bin/env python3

from gurobipy import *
input_file_path = "/Users/cassie/Dropbox/GA/Website/p0033.lp"
input_file = input_file_path.split("/")[-1]
output_file_path = "/Users/cassie/Dropbox/GA/Website"
output_file = input_file.split(".")[0]
k = int(input("Input k:")) # get value of k
model = read ("{0}".format(input_file)) 
model.optimize()
#********************************************************************************
l=0
org_obj_func = model.getObjective()
opt_val = org_obj_func.getValue()
opt_var = model.getVars()
number_of_vars = model.NumVars
org_model_sense = model.modelSense
org_obj_func_coeffs = {}
for i in range(number_of_vars):
    org_obj_func_coeffs[i] = opt_var[i].getAttr("Obj")
    #print ('org_obj_func_coeffs[i]' , org_obj_func_coeffs[i])
if (org_model_sense == -1 ):
	direction = "MAXIMIZATION"
else:
	direction = "MINIMIZATION"
model.modelSense = -1

X = {}
# print ('number_of_vars', number_of_vars)
for i in range(number_of_vars):
    X[l,i] = opt_var[i].X
for v in model.getVars():
    # print(v)
    print('%s %.2f' % (v.varName, v.x))    
print(model.objVal)     
#*****************************************************************************
X_k = {}

c = {}
s = {}
q = {}
epsilon = 1e-6

Dx_func = LinExpr()

if (org_model_sense == -1):

	for i in range(number_of_vars):
		Dx_func.addTerms(-1* org_obj_func_coeffs[i], opt_var[i])
	Dx_func_const = opt_val
	
else:

    for i in range(number_of_vars):
        Dx_func.addTerms(org_obj_func_coeffs[i], opt_var[i])
    Dx_func_const = -1 * opt_val
    
     
Dx_func.addConstant(Dx_func_const)
model.setObjective(Dx_func) #Dx_func=3.0 + -1.0 x + -1.0 y + -2.0 z
model.optimize()
MaxDx = model.objVal #MaxDx=2112.0
# ===================================checkmark==============================================#

new_constr = LinExpr()
new_constr_const = 0 
# (0, 0): 1.0, (0, 1): 0.0, (0, 2): 0.0, (0, 3): 0.0, (0, 4): 0.0, (0, 5): 0.0, (0, 6): 1.0, (0, 7): 1.0, (0, 8): 0.0, (0, 9): 1.0, (0, 10): 0.0, (0, 11): 0.0, (0, 12): 0.0, (0, 13): 1.0, (0, 14): 0.0, (0, 15): 0.0, (0, 16): 0.0, (0, 17): 1.0, (0, 18): 0.0, (0, 19): 0.0, (0, 20): 1.0, (0, 21): 1.0, (0, 22): 0.0, (0, 23): 1.0, (0, 24): 1.0, (0, 25): 1.0, (0, 26): 1.0, (0, 27): 1.0, (0, 28): 1.0, (0, 29): 1.0, (0, 30): 0.0, (0, 31): 0.0, (0, 32): 0.0}
for i in range(number_of_vars):
        
    if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I"):
            
        if X[l,i] == 0 :
            new_constr.addTerms(1.0, opt_var[i])
            
        else :
            new_constr.addTerms(-1.0, opt_var[i])
            new_constr_const = new_constr_const + 1
new_constr.addConstant(new_constr_const)
model.addConstr(new_constr, GRB.GREATER_EQUAL , 1) 
model.update()
l+=1
for i in range(number_of_vars):
    c[i] = 0
for i in range(number_of_vars):
    if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I" ) :
        for j in range(l):
            c[i] += X[j,i]
    c[i] = c[i]/l #c= {0: 1.0, 1: 0.0, 2: 1.0}
Nx_func_const = 0
Nx_func = LinExpr()
for i in range(number_of_vars):
    if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I") :
       
        Nx_func.addTerms(1 - 2*c[i], opt_var[i])
        Nx_func_const +=  c[i]
    else:
        Nx_func.addTerms(0, opt_var[i])

Nx_func.addConstant(Nx_func_const)
print(Nx_func)
model.setObjective(Nx_func)
model.optimize()  
MaxNx = Nx_func.getValue() #MaxNx = 19.0
F = MaxDx / MaxNx #F=0.666666
print(F) #111.15789473684211
for i in range(number_of_vars):
    X_k[i] = X[l-1,i] #X_k={0: 1.0, 1: 0.0, 2: 1.0}
# print(X_k)
Nx_value = Nx_func_const #15
for i in range(number_of_vars):
    s[i] = Nx_func.getCoeff(i) * X_k[i]
#     # print ('s' , i , s[i])
    Nx_value = Nx_value + s[i] #Nx_value=0
Dx_value = Dx_func_const 
for i in range(number_of_vars):
    q[i] = (Dx_func.getCoeff(i) * X_k[i])
    Dx_value = Dx_value + q[i] #Dx_value=0
Lambda = F * (Nx_value / (Dx_value + epsilon)) #Lambda =0
# print("-----")
# # <gurobi.LinExpr: 2.0 + -1.0 x + y + -1.0 z
# print(model.getObjective())
# # constant = 1.3333333333333333
DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
print(DinkleBach_func_const) #Lambda=1667.3684210526317
# print("DinkleBach_func_const",DinkleBach_func_const)
model.setAttr("ObjCon", DinkleBach_func_const) #objective function = 1.3333333333333333 + -1.0 x + y + -1.0 z
for i in range(number_of_vars):
    coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
    opt_var[i].setAttr("Obj", coef ) #objective function 1.3333333333333333 + -0.6666666666666666 x + 0.6666666666666666 y + -0.6666666666666666 z
model.update()          
model.optimize()
model.write("gurobi-p0033.lp")
# model.write("algorithm-gurobi.lp")
print("------------")
print(model.getObjective())
print(model.objVal) #objective value = 2112.0
for v in model.getVars():
    print(v.varName, v.x)
# # <gurobi.LinExpr: 1667.3684210526317 + -111.15789473684211 C157 + 111.15789473684211 C158 
# # + 111.15789473684211 C159 + 111.15789473684211 C160 + 111.15789473684211 C161 
# # + 111.15789473684211 C162 + -111.15789473684211 C163 + -111.15789473684211 C164 
# # + 111.15789473684211 C165 + -111.15789473684211 C166 + 111.15789473684211 C167 
# # + 111.15789473684211 C168 + 111.15789473684211 C169 + -111.15789473684211 C170
# #  + 111.15789473684211 C171 + 111.15789473684211 C172 + 111.15789473684211 C173 
# # + -111.15789473684211 C174 + 111.15789473684211 C175 + 111.15789473684211 C176 
# # + -111.15789473684211 C177 + -111.15789473684211 C178 + 111.15789473684211 C179
# #  + -111.15789473684211 C180 + -111.15789473684211 C181 + -111.15789473684211 C182
# #  + -111.15789473684211 C183 + -111.15789473684211 C184 + -111.15789473684211 C185 
# # + -111.15789473684211 C186 + 111.15789473684211 C187 + 111.15789473684211 C188 
# # + 111.15789473684211 C189>
# print(model.getObjective())
# print("DinkleBach_func_const",DinkleBach_func_const)
# # Nx_func <gurobi.LinExpr: 15.0 + -1.0 C157 + C158 + C159 + C160 + C161 + C162 + -1.0 C163 + -1.0 C164 + C165 + -1.0 C166 + C167 + C168 + C169 + -1.0 C170 + C171 + C172 + C173 + -1.0 C174 + C175 + C176 + -1.0 C177 + -1.0 C178 + C179 + -1.0 C180 + -1.0 C181 + -1.0 C182 + -1.0 C183 + -1.0 C184 + -1.0 C185 + -1.0 C186 + C187 + C188 + C189>
# print("Nx_func", Nx_func)
# print("MaxNx",MaxNx)
# # -3089.0 + 171.0 C157 + 171.0 C158 + 171.0 C159 + 171.0 C160 + 163.0 C161 + 162.0 C162 + 163.0 C163 + 69.0 C164 + 69.0 C165 + 183.0 C166 + 183.0 C167 + 183.0 C168 + 183.0 C169 + 49.0 C170 + 183.0 C171 + 258.0 C172 + 517.0 C173 + 250.0 C174 + 500.0 C175 + 250.0 C176 + 500.0 C177 + 159.0 C178 + 318.0 C179 + 159.0 C180 + 318.0 C181 + 159.0 C182 + 318.0 C183 + 159.0 C184 + 318.0 C185 + 114.0 C186 + 228.0 C187 + 159.0 C188 + 318.0 C18
# print("MaxDx:",MaxDx, "<Dx_func>",Dx_func)
# print("c",c)            
for i in range(number_of_vars):
    X_k[i] = opt_var[i].X
# print(model.getObjective())

# # ======================counter += 1============================================

Nx_value = Nx_func_const
print(X_k)
for i in range(number_of_vars):
    s[i] = Nx_func.getCoeff(i) * X_k[i]
    # print ('s' , i , s[i])
    Nx_value = Nx_value + s[i] #Nx_value=0
print(Nx_value) #19

Dx_value = Dx_func_const 
print(Dx_value)
print(Dx_func)
# -3089.0 + 171.0 C157 + 171.0 C158 + 171.0 C159 + 171.0 C160 + 163.0 C161 + 162.0 C162 + 163.0 C163 + 69.0 C164 + 69.0 C165 + 183.0 C166 + 183.0 C167 + 183.0 C168 + 183.0 C169 + 49.0 C170 + 183.0 C171 + 258.0 C172 + 517.0 C173 + 250.0 C174 + 500.0 C175 + 250.0 C176 + 500.0 C177 + 159.0 C178 + 318.0 C179 + 159.0 C180 + 318.0 C181 + 159.0 C182 + 318.0 C183 + 159.0 C184 + 318.0 C185 + 114.0 C186 + 228.0 C187 + 159.0 C188 + 318.0 C189>
for i in range(number_of_vars):
    q[i] = (Dx_func.getCoeff(i) * X_k[i])
    Dx_value = Dx_value + q[i] #Dx_value=0
print(Dx_value)
Lambda = F * (Nx_value / (Dx_value + epsilon))
print(Lambda)
# # print("-----")
# # # <gurobi.LinExpr: 2.0 + -1.0 x + y + -1.0 z
# # print(model.getObjective())
# # # constant = 1.3333333333333333
# # DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
# # model.setAttr("ObjCon", DinkleBach_func_const) #objective function = 1.3333333333333333 + -1.0 x + y + -1.0 z
# # for i in range(number_of_vars):
# #     coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
# #     opt_var[i].setAttr("Obj", coef ) #objective function 1.3333333333333333 + -0.6666666666666666 x + 0.6666666666666666 y + -0.6666666666666666 z
# # model.update()          
# # model.optimize() #objective value = 1655.2304880067868
# # print(model.objVal)
# # for i in range(number_of_vars):
# #     X_k[i] = opt_var[i].X
# # print(X_k) #{0: 0.0, 1: 1.0, 2: -0.0, 3: -0.0, 4: 0.0, 5: 1.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: 0.0, 10: 1.0, 11: -0.0, 12: 0.0, 13: 1.0, 14: 0.0, 15: 1.0, 16: 0.0, 17: 0.0, 18: 0.0, 19: 1.0, 20: 0.0, 21: 0.0, 22: 1.0, 23: 0.0, 24: 1.0, 25: 1.0, 26: 1.0, 27: 1.0, 28: 1.0, 29: 1.0, 30: 0.0, 31: 0.0, 32: 1.0}
# # # ======================counter += 1============================================
# # Nx_value = Nx_func_const
# # # print(Nx_value)
# # for i in range(number_of_vars):
# #     s[i] = Nx_func.getCoeff(i) * X_k[i]
# #     # print ('s' , i , s[i])
# #     Nx_value = Nx_value + s[i] #Nx_value=15
# # # print(Nx_value) 
# # Dx_value = Dx_func_const 
# # # print(Dx_value)
# # for i in range(number_of_vars):
# #     q[i] = (Dx_func.getCoeff(i) * X_k[i])
# #     Dx_value = Dx_value + q[i] #Dx_value=6
# # print(Dx_value)
# # Lambda = F * (Nx_value / (Dx_value + epsilon)) #lambda=277.89469052632353
# # # print(Lambda)
# # # print("-----")
# # # <gurobi.LinExpr: 7916.379907296874 + -457.08892888824914 C157 + -234.77313941456495 C158 + -234.77313941456495 C159 + -234.77313941456495 C160 + -218.58923138408974 C161 + -216.56624288028038 C162 + -440.90502085777393 C163 + -250.74410149969057 C164 + -28.428312026006353 C165 + -481.3647909339619 C166 + -259.04900146027774 C167 + -259.04900146027774 C168 + -259.04900146027774 C169 + -210.2843314235026 C170 + -259.04900146027774 C171 + -410.77313924598263 C172 + -934.7271617326167 C173 + -616.9050206891916 C174 + -900.3363571678569 C175 + -394.5892312155074 C176 + -1122.652146641541 C177 + -432.8130668425364 C178 + -532.1524494745465 C179 + -432.8130668425364 C180 + -754.4682389482307 C181 + -432.8130668425364 C182 + -754.4682389482307 C183 + -432.8130668425364 C184 + -754.4682389482307 C185 + -341.7785841711135 C186 + -350.08348413170063 C187 + -210.4972773688522 C188 + -532.1524494745465 C189>
# # print(model.getObjective())
# # # # constant = 1.3333333333333333
# # # DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
# # # model.setAttr("ObjCon", DinkleBach_func_const) #objective function = 1.3333333333333333 + -1.0 x + y + -1.0 z
# # # for i in range(number_of_vars):
# # #     coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
# # #     opt_var[i].setAttr("Obj", coef ) #objective function 1.3333333333333333 + -0.6666666666666666 x + 0.6666666666666666 y + -0.6666666666666666 z
# # # model.update()          
# # # model.optimize()
# # # print(model.objVal)
# # # for i in range(number_of_vars):
# # #     X_k[i] = opt_var[i].X
# # # ======================counter += 1============================================
# # # Nx_value = Nx_func_const
# # # for i in range(number_of_vars):
# # #     s[i] = Nx_func.getCoeff(i) * X_k[i]
# # #     # print ('s' , i , s[i])
# # #     Nx_value = Nx_value + s[i] #Nx_value=0
# # # Dx_value = Dx_func_const 
# # # for i in range(number_of_vars):
# # #     q[i] = (Dx_func.getCoeff(i) * X_k[i])
# # #     Dx_value = Dx_value + q[i] #Dx_value=0
# # # Lambda = F * (Nx_value / (Dx_value + epsilon))
# # # print("-----")
# # # # <gurobi.LinExpr: 2.0 + -1.0 x + y + -1.0 z
# # # print(model.getObjective())
# # # # constant = 1.3333333333333333
# # # DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
# # # model.setAttr("ObjCon", DinkleBach_func_const) #objective function = 1.3333333333333333 + -1.0 x + y + -1.0 z
# # # for i in range(number_of_vars):
# # #     coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
# # #     opt_var[i].setAttr("Obj", coef ) #objective function 1.3333333333333333 + -0.6666666666666666 x + 0.6666666666666666 y + -0.6666666666666666 z
# # # model.update()          
# # # model.optimize()
# # # print(model.objVal)
# # # for i in range(number_of_vars):
# # #     X_k[i] = opt_var[i].X
# # # model.write("algorithm-gurobi.lp")