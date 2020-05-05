#!/usr/bin/env python3

from gurobipy import *
input_file="p0033.lp"
model = read ("{0}".format(input_file)) 
model.optimize()
#********************************************************************************
l=0
org_obj_func = model.getObjective()
# objective value
opt_val = org_obj_func.getValue()
# get variables
opt_var = model.getVars()
# get number of vars
number_of_vars = model.NumVars
# get model sense
org_model_sense = model.modelSense
# get coefficients of the objective function
org_obj_func_coeffs = {}
for i in range(number_of_vars):
    org_obj_func_coeffs[i] = opt_var[i].getAttr("Obj")
if (org_model_sense == -1):
	direction = "MAXIMIZATION"
else:
	direction = "MINIMIZATION"
model.modelSense = -1
X = {}
for i in range(number_of_vars):
    X[l,i] = opt_var[i].X   
# get objective value
# print(model.objVal)     
# #*****************************************************************************
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
model.setObjective(Dx_func) 
model.optimize()
MaxDx = model.objVal
# # ===================================checkmark==============================================#

new_constr = LinExpr()
new_constr_const = 0 
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
model.optimize()
l+=1
for i in range(number_of_vars):
    c[i] = 0
for i in range(number_of_vars):
    if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I" ) :
        for j in range(l):
            c[i] += X[j,i]
    c[i] = c[i]/l 
Nx_func = LinExpr()
for i in range(number_of_vars):
    if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I") :
       
        Nx_func.addTerms(1 - 2*c[i], opt_var[i])
        Nx_func_const +=  c[i]
    else:
        Nx_func.addTerms(0, opt_var[i])

Nx_func.addConstant(Nx_func_const)
model.setObjective(Nx_func)
model.optimize()  

MaxNx = Nx_func.getValue() 
F = MaxDx / MaxNx  
for i in range(number_of_vars):
    X_k[i] = X[l-1,i]
Nx_value = Nx_func_const
for i in range(number_of_vars):
    s[i] = Nx_func.getCoeff(i) * X_k[i]
    Nx_value = Nx_value + s[i]
Dx_value = Dx_func_const 
for i in range(number_of_vars):
    q[i] = (Dx_func.getCoeff(i) * X_k[i])
    Dx_value = Dx_value + q[i]
Lambda = F * (Nx_value / (Dx_value + epsilon))
DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
model.setAttr("ObjCon", DinkleBach_func_const) 
model.optimize()
for i in range(number_of_vars):
    coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
    opt_var[i].setAttr("Obj", coef ) 
model.update()          
model.optimize()
for i in range(number_of_vars):
    X_k[i] = opt_var[i].X

# # # # ======================counter += 1============================================

Nx_value = Nx_func_const

for i in range(number_of_vars):
    s[i] = Nx_func.getCoeff(i) * X_k[i]
    Nx_value = Nx_value + s[i] 

Dx_value = Dx_func_const 

for i in range(number_of_vars):
    q[i] = (Dx_func.getCoeff(i) * X_k[i])
    Dx_value = Dx_value + q[i] 
Lambda = F * (Nx_value / (Dx_value + epsilon))
DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))

for i in range(number_of_vars):
    coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
    opt_var[i].setAttr("Obj", coef ) 
model.update()          
model.optimize() 
for i in range(number_of_vars):
    X_k[i] = opt_var[i].X
# ======================counter += 1============================================
