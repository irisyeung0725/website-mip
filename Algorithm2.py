# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 18:04:05 2017

@author: Narge
"""

from gurobipy import *
import sys
from time import gmtime, strftime
import os
l = 0 


#Read and Solve primary model


# if (len(sys.argv) < 3):

# 	if (len(sys.argv) < 2):
#         # it has to be .lp or .mps file
# 		print('Please Enter Your LP/MPS File and K')
# 	else:
# 		print('Please Enter K')
		
# 	quit()

input_file_path = "/Users/cassie/Dropbox/GA/Website/p0033.lp"
input_file = input_file_path.split("/")[-1]
output_file_path = "/Users/cassie/Dropbox/GA/Website"
output_file = input_file.split(".")[0]
k = int(input("Input k:")) # get value of k
model = read ("{0}".format(input_file)) 
model.optimize()

#********************************************************************************
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
              

#*****************************************************************************
input_file_name = os.path.basename(input_file)
output_file_name = input_file_name.split(".")[0]
f = open ("{0}/{1}_test.out".format(output_file_path,output_file_name), 'w')
f.write ("Local date and time is: {0} \n\n".format (strftime("%a, %d %b %Y %H:%M:%S ", gmtime())))
f.write ( "Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file_name))
f.write ( "Original objective function direction is {0}\n".format(direction))
f.write ("Diversity metric is to maximize distance from centroid\n\n")
f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
f.write ("N/A          N/A        %10.5f         0                  0              " %(opt_val))
for i in range(number_of_vars):
			f.write("%.0f" %abs(X[l,i])) 
f.write ("\n")


#******************************************************************************



# print ('***********************************')
# print (org_obj_func)
# print('opt_val' , opt_val) 

# for i in range(number_of_vars):
   # print(opt_var[i].VarName , opt_var[i].X)
  
#==============================================================================
# for i in range(number_of_binary_vars):
#    print(X_B[l,i])
#==============================================================================
     
# print ('***********************************')

X_k = {}

c = {}
s = {}
q = {}

# for i in range(number_of_vars):
	# c[i] = 0
	# s[i] = 0
	# q[i] = 0

 #build and solve Max_D(x) --> z* - Cx maximization and Cx - z* for minimization
 
#org_obj_func_coeffs[i]
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

# print ('**************************************')
#print ("Dx_func = " , Dx_func)
# print('MaxDx' , MaxDx) 
# for i in range(number_of_vars):
    # print(opt_var[i].VarName , opt_var[i].X) 
# print ('*************************************')

# iterations = {}
# OptObjVal = {}
# GapOffOptimal ={}
# DiversityMeasure = {}

# for j in range(k+1):
	# iterations[j] = 0
	# OptObjVal[j] = 0
	# GapOffOptimal[j] = 0
	# DiversityMeasure[j] = 0
			




while (l < k):
    #Add new constraint
    
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
    
    
#==============================================================================
#      u = model.getConstrs()[1]
#      print ( model.getRow(u) , u.getAttr("Sense") , u.getAttr("RHS") )
#     
#==============================================================================
            
    l = l + 1
    
    #==============================================================================
    # for i in range(number_of_vars):
    #     X[l,i] = 1
    #      
    # l = l + 1     
    #==============================================================================
    #calculate centeroid

       
    for i in range(number_of_vars):
        c[i] = 0
    
    for i in range(number_of_vars):
        if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I" ) :
            for j in range(l):
                c[i] += X[j,i]
        
           
                
        c[i] = c[i]/l
	
         
    # print ('centeroid' , c)  
      
    #build and solve Max_N(x) 
    
    Nx_func_const = 0
    Nx_func = LinExpr()
    for i in range(number_of_vars):
        
        if (opt_var[i].vtype == "B" or opt_var[i].vtype == "I") :
       
            Nx_func.addTerms(1 - 2*c[i], opt_var[i])
            Nx_func_const +=  c[i]
        else:
            Nx_func.addTerms(0, opt_var[i])
         
    Nx_func.addConstant(Nx_func_const) 
     
    model.setObjective(Nx_func)
	#print ('Nx_func' , Nx_func)
    model.optimize()  
    MaxNx = Nx_func.getValue()  
    
    
    # print ('*************************************')
    #print (Nx_func)
    # print('MaxNx' , MaxNx) 
    # for i in range(number_of_vars):
        # print(opt_var[i].VarName , opt_var[i].X)
    # print ('*************************************')
    
    
      
    #calculat F  
    F = MaxDx / MaxNx
    # print ('****************************************')
    # print ('F=' , F)
    # print ('****************************************')
    
    epsilon = 1e-6
    
    
    
    for i in range(number_of_vars):
        
        X_k[i] = X[l-1,i]
        #print (X_k[i])
	    
       
         
    true = 1
    
    counter = 0
    
    while true:
        
        counter = counter + 1
        #print ('****************************************')
        #print ('k = {0} , Iteration +{1}:'.format(l,counter))
		
       
    #Calculate Nx
        
        Nx_value = Nx_func_const
        # print ('Nx_func_const' , Nx_func_const)
        for i in range(number_of_vars):
            
                s[i] = Nx_func.getCoeff(i) * X_k[i]
                # print ('s' , i , s[i])
                Nx_value = Nx_value + s[i]
        
        # print ('Nx_value for X_K' , Nx_value)
       
    #Calculate Dx 
        
       
        Dx_value = Dx_func_const 
         
        for i in range(number_of_vars):
             q[i] = (Dx_func.getCoeff(i) * X_k[i])
             Dx_value = Dx_value + q[i]
        
        # print ('Dx_value for X_K' , Dx_value)
        
               
    #Calculate Landa
        
        Lambda = F * (Nx_value / (Dx_value + epsilon))    
        #print('Lambda' , Lambda)
        
       
    
    #************************************make F*N(x) - Landa*D(x)
    
        DinkleBach_func_const = (F * Nx_func_const) - (Lambda * (Dx_func_const + epsilon ))
        #print ('DinkleBach_func_const' , DinkleBach_func_const)
        
        model.setAttr("ObjCon", DinkleBach_func_const) 
       
        for i in range(number_of_vars):
            coef = (F * Nx_func.getCoeff(i))  - (Lambda * Dx_func.getCoeff(i) ) 
            opt_var[i].setAttr("Obj", coef )
            
        model.update()  
           
    #    print ('F*N(x) - Landa*D(x)' , model.getObjective())  
        # print ('***********************************')
        model.optimize()
       
	   
        if( -0.001 <= model.objVal <= 0.001):
            
							
			# iterations[l] = counter
			# GapOffOptimal[l] = Dx_value
			# DiversityMeasure[l] = Nx_value
			# OptObjVal[l] = abs(opt_val - Dx_value)
			
			# print ('*******************************')
            # print ("obj function is equal to Zero at iteration %d and K= %d" %(counter,l) )
            # print ('objval' , model.objVal )
            # print ('****************************')
            for i in range(number_of_vars):
                X[l,i] = opt_var[i].X
            f.write ("%3d          %3d        %10.5f      %10.5f         %10.5f        " %(l,counter,abs(opt_val - Dx_value),Dx_value,Nx_value))
            for i in range(number_of_vars):
                f.write("%.0f" %abs(X[l,i])) 
            f.write ("\n")
            
            true = 0
        else:
            # print ('*********************************')
            # print ( 'obj function is NOT equal to Zero' )
            # print ('objval' , model.objVal )
      
            for i in range(number_of_vars):
                X_k[i] = opt_var[i].X
            
    #        print ('X_k' , X_k)
    
      
 
   
           
    # print('optimal value is:') 
           
    # for j in range(l+1):
        # if (j != 0): 
            # print('Near optimal solution '+str(j)+' is:')
   
        # for i in range(number_of_vars):
            # print(X[j,i])

			

    

    
f.close()



	
