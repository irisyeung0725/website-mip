
import glpk
import os
import pdb
import sys
from time import gmtime, strftime

# **************************************************
# IT IS NOT DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  *
# **************************************************

"""

pdb.set_trace()
problem = glpk("/home/narges/Documents/Knapsack.lp")
problem.update()
problem.solve() 

print "problem.solution =" , problem.solution()

number_of_vars = glp_get_num_cols(problem._lp)
org_model_sense = glp_get_obj_dir(problem._lp)
opt_val = glp_get_obj_val(problem._lp)

print "number_of_vars" ,number_of_vars
print "org_model_sense" ,org_model_sense
print "opt_val" , opt_val

"""


l = 0 
k = 4
# if (len(sys.argv) < 2):
#     print('Please Enter your LP/MPS file and K')
#     quit()

# input_file = sys.argv[1]
# # k = int(sys.argv[2])

output_file_path = "/Users/cassie/Dropbox/GA/Website/"

# # problem = glpk.LPX()

# file_extension = input_file.split("/")[-1]

# if file_extension.split(".")[-1] == "lp":
#     lp = glpk.LPX(cpxlp=input_file)
# elif file_extension.split(".")[-1] == "mps":
#     lp = glpk.LPX(mps=input_file)
# else:
#     print("We only accept lp/mps file")
#     quit()

input_file = "/Users/cassie/Dropbox/GA/Website/mip1.lp"
lp = glpk.LPX(cpxlp=input_file)

lp.simplex()                        # Solve this LP with the simplex method
# *-------------------------------------------------------------------------------------------------------------*
# glp_read_lp(problem,None, "{0}".format(input_file))

# glp_read_lp(problem,None, "/home/narges/Documents/Knapsack.lp") 
# glp_read_mps(problem, GLP_MPS_FILE , None, "/home/narges/Documents/p0033.mps") 


# parm = glp_iocp()
# glp_init_iocp(parm)
# parm.presolve = 1
# glp_intopt(problem, parm)
# *-------------------------------------------------------------------------------------------------------------*

opt_val = lp.obj.value
org_model_sense = lp.obj.maximize
opt_var = lp.cols
number_of_vars = lp.nint # number of vars
org_obj_func_coeffs = {} # get coefficients
for i in range(number_of_vars):
    org_obj_func_coeffs[i] = lp.obj[i]
if (org_model_sense == True ):
	direction = "MAXIMIZATION"
else:
	direction = "MINIMIZATION"

org_model_sense = True
X = {}
for i in range(number_of_vars):
    X[l,i] = opt_var[i].primal

# *-------------------------------------------------------------------------------------------------------------*
input_file_name = os.path.basename(input_file)
output_file_name = input_file_name.split(".")[0]
f = open ("{0}/{1}.txt".format(output_file_path,output_file_name), 'w')
f.write ("Local date and time is: {0} \n\n".format (strftime("%a, %d %b %Y %H:%M:%S ", gmtime())))
f.write ( "Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file_name))
f.write ( "Original objective function direction is {0}\n".format(direction))
f.write ("Diversity metric is to maximize distance from centroid\n\n")
f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
f.write ("N/A          N/A        %10.5f         0                  0              " %(opt_val))
for i in range(number_of_vars):
			f.write("%.0f" %abs(X[l,i])) 
f.write ("\n")
# *-------------------------------------------------------------------------------------------------------------*

X_k = {}

c = {}
s = {}
q = {}

#build and solve Max_D(x) --> z* - Cx maximization and Cx - z* for minimization
Dx_obj_list = []
# Dx_func = glpk.LPX()
Dx_func = lp
if (org_model_sense == True):
    # Dx_func.cols.add(number_of_vars)
    for i in range(number_of_vars):
        # Dx_func.cols[i] = lp.cols[i].name 
        Dx_obj_list.append(-1* org_obj_func_coeffs[i])
    Dx_func.obj[:] = Dx_obj_list
    Dx_func_const = opt_val
else:
    for i in range(number_of_vars):
        # Dx_func.cols[i] = lp.cols[i].name 
        Dx_obj_list.append(org_obj_func_coeffs[i])
    Dx_func.obj[:] = Dx_obj_list
    Dx_func_const = opt_val

# col = [0] * lp.nint
# for i in col:
#     del(lp.cols[i]) # delete old lp model but constraints remain (hopefully)
Dx_func.obj[:] = Dx_obj_list
Dx_func.obj[None] = Dx_func_const # append constant to the objective function
Dx_func.simplex()
Dx_Max = Dx_func.obj.value
# *-------------------------------------------------------------------------------------------------------------*
# remake the constraint matrix from input model
import numpy as np

matrix = np.array(Dx_func.matrix)
len_matrix = len(matrix)
number_of_rows = len(Dx_func.rows)
# set not showing value to 0
mat = np.zeros((number_of_rows,number_of_vars)) 
print(matrix)
print(len(matrix))
print(number_of_rows)
print(mat)
# for i in range(len_matrix): #lenth of 5
#     print(i)
#     for j in range(len(matrix)-1): #lenth of 4
#         # print(int(matrix[i,0]),int(matrix[i,1]),matrix[i,2])
#         print(mat[int(matrix[i,0]),int(matrix[i,1])])
for i in range(len_matrix):
    for j in range(len(matrix)-1):
        mat[int(matrix[i,0]),int(matrix[i,1])] = matrix[i,2]
# return a list of constraint coefficients (including 0 value)
mat = list(np.ravel(mat)) 
# *-------------------------------------------------------------------------------------------------------------*

# Constraint_list = []
while (l < k):
    #Add new constraint
    # new_constr = glpk.LPX()
    new_constr_const = 0 
    # constraint_coeff_list = []
    for i in range(number_of_vars):
        Dx_func.rows.add(1)
        if opt_var[i].kind == bool or opt_var[i].kind == int:
            if X[l,i] == 0:
                mat.append(1.0) # append value to the matrix list
                
            else:
                mat.append(-1.0)
                new_constr_const = new_constr_const + 1
        else:
            mat.append(0.0) # set 0 value for not valid retults
    # new_constr.obj[None] = new_constr_const
    # new_constr.obj[:] = Constraint_col_list
    Dx_func.rows[-1].bounds = (1 - new_constr_const), None
# *-------------------------------------------------------------------------------------------------------------*
    l += 1

    for i in range(number_of_vars):
        c[i] = 0
    
    for i in range(number_of_vars):
        if opt_var[i].kind == bool or opt_var[i].kind == int:
            for j in range(l):
                c[i] += X[j,i]

        c[i] = c[i]/l
# *-------------------------------------------------------------------------------------------------------------*
    Nx_obj_list = []
    Nx_func_const = 0
    Nx_func = Dx_func
    for i in range(number_of_vars):
        if opt_var[i].kind == bool or opt_var[i].kind == int:
            Nx_obj_list.append(float(1 - 2*c[i]))
            Nx_func_const +=  c[i]
        else:
            Nx_obj_list.append(0.0)
    Nx_func.obj[:] = Nx_obj_list
    Nx_func.obj[None] = Nx_func_const # append constant to the objective function
    Nx_func.simplex()
    Nx_Max = Nx_func.obj.value
# *-------------------------------------------------------------------------------------------------------------*
    # Calculate F
    F = Dx_Max / Nx_Max
# *-------------------------------------------------------------------------------------------------------------*
    epsilon = 1e-6
    for i in range(number_of_vars): 
        X_k[i] = X[l-1,i]

    true = 1
    counter = 0
    while true:
        counter = counter + 1
        # Calculate Nx
        Nx_value = Nx_func_const
        for i in range(number_of_vars):
            s[i] = Nx_obj_list[i] * X_k[i]
            Nx_value = Nx_value + s[i]
        # Calculate Dx
        Dx_value = Dx_func_const
        for i in range(number_of_vars):
            q[i] = Dx_obj_list[i] * X_k[i]
            Dx_value = Dx_value + q[i]
        # Calculate Lambda
        Lambda = F * ( Nx_value / (Dx_value + epsilon)) 
# *-------------------------------------------------------------------------------------------------------------*
        # make F*N(x) - Landa*D(x)
        DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon))
        Nx_func.obj[None] = DinkleBach_func_const # set new constant to the objective function
        DinkleBach_func = Nx_func
        DinkleBach_func_list = []
        for i in range(number_of_vars):
            coef = (F * Nx_obj_list[i])  - (Lambda * Dx_obj_list[i])
            DinkleBach_func_list.append(coef)
        DinkleBach_func.obj[:] = DinkleBach_func_list
        print(len(DinkleBach_func_list))
        DinkleBach_func.exact()

        if( -0.001 <= DinkleBach_func.obj.value <= 0.001):
            for i in range(number_of_vars):
                X[l,i] = DinkleBach_func.obj[i]
                f.write ("%3d          %3d        %10.5f      %10.5f         %10.5f        " %(l,counter,abs(opt_val - Dx_value),Dx_value,Nx_value))
            for i in range(number_of_vars):
                f.write("%.0f" %abs(X[l,i])) 
            f.write ("\n")

            true = 0
        else:
            X_k[i] = DinkleBach_func.obj[i]
f.close()


# #print "org_model_sense" , org_model_sense 
# glp_set_obj_dir(problem, GLP_MAX)


# number_of_vars = glp_get_num_cols(problem)
# #print "number_of_vars" ,number_of_vars

# number_of_rows = glp_get_num_rows(problem)
# #print "number_of_rows" , number_of_rows



# var_type = {}
# for i in range(number_of_vars):
#     var_type[i] = glp_get_col_kind(problem, i+1)
# print("var_type" , var_type)
   

# org_opt_sol = glp_mip_obj_val(problem)
# #print "org_opt_sol" , org_opt_sol

# X = {}
# for i in range(number_of_vars):
#     X[l,i] = glp_mip_col_val(problem, i+1)
#     #print "org_opt_var_val[%g,%g]=%g" %(l,i,X[l,i])


# org_obj_coef = {}
# for i in range(number_of_vars+1):
#     org_obj_coef[i] = glp_get_obj_coef(problem, i)
#    # print "org_obj_coef[%g]=%g" %(i,org_obj_coef[i])
# #print "org_obj_coef=" , org_obj_coef

# #glp_write_lp(problem, None, "/home/narges/Documents/Knapsack_output.lp")



# input_file_name = os.path.basename(input_file)
# output_file_name = input_file_name.split(".")[0]
# f = open ("{0}\{1}.txt".format(output_file_path,output_file_name), 'w')
# f.write ("Local date and time is: {0} \n\n".format (strftime("%a, %d %b %Y %H:%M:%S ", gmtime())))
# f.write ( "Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file_name))
# f.write ( "Original objective function direction is {0}\n".format(org_model_sense))
# f.write ("Diversity metric is to maximize distance from centroid\n\n")
# f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
# f.write ("N/A          N/A        %10.5f         0                  0            " %(org_opt_sol))
# for i in range(number_of_vars):
# 			f.write("%.0f" %abs(X[l,i])) 
# f.write ("\n")



# #----------------------------------------build and solve Max_D(x) --> z* - Cx maximization and Cx - z* for minimization
# Dx_coef = {}

# if (org_model_sense == 2):
#     for i in range(1 , number_of_vars+1 ):
#         Dx_coef[i] = -1 * org_obj_coef[i]
#     Dx_coef[0] = org_opt_sol
# else:
#     if (org_model_sense == 1):
#         for i in range(1 , number_of_vars+1 ):
#             Dx_coef[i] = org_obj_coef[i]
#         Dx_coef[0] = -1 * org_opt_sol    

# for i in range(number_of_vars+1):
#     glp_set_obj_coef(problem, i, Dx_coef[i])

# glp_intopt(problem, parm)

# Max_Dx_opt_sol = glp_mip_obj_val(problem)
# #print "Max_Dx_opt_sol" , Max_Dx_opt_sol

# Max_Dx_opt_var_val = {}
# for i in range(number_of_vars):
#     Max_Dx_opt_var_val[i] = glp_mip_col_val(problem, i+1)
#    # print "Max_Dx_opt_var_val[%g]=%g" %(i,Max_Dx_opt_var_val[i])

# Max_Dx_obj_coef = {}
# for i in range(number_of_vars+1):
#     Max_Dx_obj_coef[i] = glp_get_obj_coef(problem, i)
#   #  print "Max_Dx_obj_coef[%g]=%g" %(i,Max_Dx_obj_coef[i])
# #print "Max_Dx_obj_coef=" , Max_Dx_obj_coef
# #-------------------------------------------------------------------------------------
# size = number_of_vars +1
# new_cnstr_var_indis = intArray(size)
# new_cnstr_coefs = doubleArray(size)
# c = {}
# x_k = {}
# s = {}



		

# while (l < k):

# #---------------------------------------------------Add new constrain
#     new_cnstr_const = 0
#     glp_add_rows(problem, 1)
#     number_of_rows += 1
        

#     for i in range(number_of_vars):

#         new_cnstr_var_indis[i+1] = i+1
#         if (var_type[i] == 2 or var_type[i] == 3): 

#             if (X[l,i] == 0):      
#                 new_cnstr_coefs[i+1] = 1
#             else:
#                 new_cnstr_coefs[i+1] = -1
#                 new_cnstr_const += 1

    
#     glp_set_mat_row(problem, number_of_rows, number_of_vars , new_cnstr_var_indis ,new_cnstr_coefs)  
#     glp_set_row_bnds(problem, number_of_rows, GLP_LO, (1 - new_cnstr_const), 0.0)
#    # print "new constrain (number %g) has been added" %(number_of_rows)

# #---------------------------------------------------------------------------------------------
    
#     l = l + 1

# #-------------------------------------------calculate centeroid

#     for i in range(number_of_vars):
#         c[i] = 0
    
#     for i in range(number_of_vars):
#         if (var_type[i] == 2 or var_type[i] == 3) :
#             for j in range(l):
#                 c[i] += X[j,i] 
                
#         c[i] = c[i]/l
         
#     #print ('centeroid' , c) 
# #---------------------------------------build and solve Max_N(x)

#     Nx_coef = {}
#     Nx_coef[0] = 0

#     for i in range(number_of_vars):

#         if (var_type[i] == 2 or var_type[i] == 3) : 
#             Nx_coef[i+1] = 1 - 2*c[i]
#             Nx_coef[0] += c[i]
#         else:
#             Nx_coef[i+1] = 0

#         glp_set_obj_coef(problem, i+1, Nx_coef[i+1])

#     glp_set_obj_coef(problem, 0, Nx_coef[0])   

#     glp_intopt(problem, parm)

#     Max_Nx_opt_sol = glp_mip_obj_val(problem)
#     #print "Max_Nx_opt_sol" , Max_Nx_opt_sol

#     Max_Nx_opt_var_val = {}
#     for i in range(number_of_vars):
#         Max_Nx_opt_var_val[i] = glp_mip_col_val(problem, i+1)
#     #print "Max_Nx_opt_var_val[%g]=%g" %(i,Max_Nx_opt_var_val[i])

#     Max_Nx_obj_coef = {}
#     for i in range(number_of_vars+1):
#         Max_Nx_obj_coef[i] = glp_get_obj_coef(problem, i)
#   # print "Max_Nx_obj_coef[%g]=%g" %(i,Max_Nx_obj_coef[i])
#     #print "Max_Nx_obj_coef=" , Max_Nx_obj_coef

# #c-------------------------------------------alculat F  
#     F = Max_Dx_opt_sol / Max_Nx_opt_sol
#     #print "F=" ,F

#     epsilon = 1e-6
      
    
#     for i in range(number_of_vars):
#        x_k[i] = X[l-1,i]
       
#     #print "x_k=" , x_k     
#     true = 1
    
#     counter = 0

#     while true:
        
#         counter = counter + 1
#         #print ('****************************************')
#         #print ('round number:' , counter)
        

#         #Calculate Nx
        
#         Nx_value = Nx_coef[0]
        
#         for i in range(number_of_vars):
            
#                 s[i] = Nx_coef[i+1] * x_k[i]
#                 Nx_value = Nx_value + s[i]
        
#         #print ('Nx_value for X_K' , Nx_value)


#         #Calculate Dx
        
#         Dx_value = Dx_coef[0]
        
#         for i in range(number_of_vars):
            
#                 s[i] = Dx_coef[i+1] * x_k[i]
#                 Dx_value = Dx_value + s[i]
        
#         #print ('Dx_value for X_K' , Dx_value)

#         #Calculate Landa
        
#         Lambda = F * ( Nx_value / (Dx_value + epsilon))    
#        # print('Lambda' , Lambda)

#  #************************************make F*N(x) - Landa*D(x)
#         DinkleBach_func_coef = {}

#         DinkleBach_func_coef[0] = (F * Nx_coef[0]) - (Lambda * (Dx_coef[0] + epsilon ))
#         glp_set_obj_coef(problem, 0, DinkleBach_func_coef[0])       
          
#         for i in range(number_of_vars):
#             DinkleBach_func_coef[i+1] = (F * Nx_coef[i+1])  - (Lambda * Dx_coef[i+1] ) 
#             glp_set_obj_coef(problem, i+1, DinkleBach_func_coef[i+1])   

#         glp_intopt(problem, parm)

#         DinkleBach_func_opt_sol = glp_mip_obj_val(problem)
        

#         DinkleBach_func_opt_var_val = {}
#         for i in range(number_of_vars):
#             DinkleBach_func_opt_var_val[i] = glp_mip_col_val(problem, i+1)
    

#         if ( - 0.001 <= DinkleBach_func_opt_sol <= 0.001):
#             for i in range(number_of_vars):
#                 X[l,i] =  DinkleBach_func_opt_var_val[i]
#             f.write ("%3d          %3d        %10.5f      %10.5f         %10.5f        " %(l,counter,abs(org_opt_sol - Dx_value),Dx_value,Nx_value))
#             for i in range(number_of_vars):
#                 f.write("%.0f" %abs(X[l,i])) 
#             f.write ("\n")	
#             true = 0
#         else:
            
#             #print ( 'obj function is NOT equal to Zero, countinue with next x_k' )
#             #print ('objval' , DinkleBach_func_opt_sol )
      
#             for i in range(number_of_vars):
#                 x_k[i] = DinkleBach_func_opt_var_val[i]

# f.close()



