#!/usr/bin/env python3

from mip import *
import sys
import os
from datetime import datetime
import signal
import fileinput

##-- find local time
current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

##-- check to see if input file and k is passed to script and load them
##-- this part is not needed since Prachi is checking
if (len(sys.argv)<3):
    if len(sys.argv)<2:
        print("please upload a lp/mps file")
    else:
        print('please enter a k (a number)')
    quit()

## ---------------------------------handle user input and output---------------------------------
input_file = sys.argv[1]
k = int(sys.argv[2])
##-- creating output file name based inpput file name
output_file_path = "/Users/cassie/Dropbox/GA/Website/"
input_file_name = os.path.basename(input_file)
output_file_name = input_file_name.split(".")[0]
##-- check if file format .lp/.mps is correct
##-- this part is not needed if Prachi is checking file format
##-- But I still check it as now I have access to output file based on input file name

if (input_file_name.split('.')[-1])!="lp" and (input_file_name.split('.')[-1])!="mps":
    f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'w')
    f.write ("Local date and time is: {0} \n\n".format (current_time))
    f.write("Input file format is incorrect. only .lp/.mps formats are acceptable.")
    f.close()
    quit()

# ##-- add this is line to handle "obj:" without space to avoid potential conflicts from cbc solver
for line in fileinput.input(input_file, inplace=1):
    sys.stdout.write(line.replace('obj:', ' '))
##-- claim cbc solver 
m = Model(solver_name=CBC)
##-- read input file
m.read(input_file)
##-- optimize original model
m.optimize()
status = m.optimize()
##-- terminate it if the orininal model is infeasible
if status != OptimizationStatus.OPTIMAL:
    f = open("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
    f.write("All feasible solutions have been identified. Present model is infeasible.")
    f.close()
    quit()

def AlgorithmII():
    ##-- define variables
    l=0
    X={}
    X_k={}
    c={}
    s={}
    q={}
    # do = float(2)
    epsilon=1e-6
    # num_binary_vars = 0 
    ##-- obtain information from the original model
    opt_val = m.objective_value # get objective value
    number_of_vars = len(m.vars) # get number of vars
    org_model_sense = m.sense # get objective sense
    org_obj_func_coeffs = {} # get coefficients for each variable from the objective function
    for i in range(number_of_vars):
        org_obj_func_coeffs[i]=m.vars[i].obj
    if org_model_sense == "MAX":
        direction = "MAXIMIZATION"
    else:
        direction = "MINIMIZATION"
    # m.sense = "MAX" # set model sense back to maximization
    for i in range(number_of_vars):
        X[l,i] = m.vars[i].x
    ##-- start creating output text file that contains basic information about the orginal model
    f = open("{0}/{1}.out".format(output_file_path,output_file_name), 'w')
    f.write("Local date and time is: {0} \n\n".format(current_time))
    f.write("Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file))
    f.write ("Original objective function direction is {0}\n".format(direction))
    f.write ("Diversity metric is to maximize distance from centroid\n\n")
    f.write ("No(k)   Iterations        OptObjVal   GapOffOptimal   DiversityMeasure       Solution\n\n")
    f.write ("N/A          N/A        %10.5f         0                  0              " %(opt_val))
    for i in range(number_of_vars):
	    f.write("%.0f" %abs(X[l,i])) 
    f.write ("\n")

    # for i in range(number_of_vars):
    #     if (m.vars[i].var_type == "B") or (m.vars[i].var_type == "I"):
    #         number_of_vars +=1

    ##-- build and solve Max_D(x) --> z* - Cx maximization and Cx - z* for minimization
    Dx_func = LinExpr()
    if org_model_sense == "MAX":
        for i in range(number_of_vars):
            Dx_func.add_term(m.vars[i],coeff=-1*org_obj_func_coeffs[i])
        Dx_func_const = opt_val
    else:
        for i in range(number_of_vars):
            Dx_func.add_term(m.vars[i],coeff =1*org_obj_func_coeffs[i])
        Dx_func_const = -1*opt_val
    Dx_func.add_const(Dx_func_const) # add constant

    m.objective = maximize(Dx_func)
    m.optimize() # optimize the model again

    ##-- check and terminate if new model is infeasible
    status = m.optimize()
    if status != OptimizationStatus.OPTIMAL:
        f = open("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
        f.write("All feasible solutions have been identified. Present model is infeasible.")
        f.close()
        quit()
    MaxDx = m.objective_value

    ##-- start while loop to find k diverse solution
    while (l < k):
        # Add new constraints
        new_constr = LinExpr()
        new_constr_const = 0
        for i in range(number_of_vars):
            if (m.vars[i].var_type == "B") or (m.vars[i].var_type == "I"):
                if X[l,i] == 0:
                    new_constr.add_term(m.vars[i],coeff=1)
                else:
                    new_constr.add_term(m.vars[i],coeff=-1)
                    new_constr_const += 1
        new_constr.add_const(new_constr_const)
        m.add_constr(new_constr >= 1)

        # increase l
        l = l + 1

        # calculate centroid
        for i in range(number_of_vars):
            c[i] = 0 
        for i in range(number_of_vars):
            if (m.vars[i].var_type == "B") or (m.vars[i].var_type =="I"):
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
            f = open("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
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
            
            m.optimize() # optimize the model 

            # calculate DiversityMeasure
            # Dbin_ = float(0)
            # for i in range(number_of_vars):
            #     if (m.vars[i].var_type == "B") or (m.vars[i].var_type =="I"):
            #         for j in range(l):
            #             for w in range(j+1, l+1):
            #                 Dbin_ += abs(X[j,i]-X[w,i])
            # Dbin = Dbin_ * do / (num_binary_vars*(l+1)*l)

            # check if max value for F*N(x) - Landa*D(x) == Zero
            # if YES then this is new diverse optimal solution
            if (-0.001 <= m.objective_value <= 0.001):
                for i in range(number_of_vars):
                    X[l,i] = m.vars[i].x
                f.write ("%3d          %3d        %10.5f      %10.5f         %10.5f        " %(l,counter,abs(opt_val - Dx_value),abs(Dx_value/(epsilon+opt_val)),Nx_value))
                for i in range(number_of_vars):
                    f.write("%.0f" %abs(X[l,i])) 
                f.write ("\n")

                true = 0 # terminate the while loop
            else:
                for i in range(number_of_vars):
                    X_k[i]=m.vars[i].x
    f.close()

def handler(signum, frame):
    f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
    f.write ("The search was prematurely terminated, because the time limit has been exceeded.")
    f.close()
    raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)
signal.alarm(500) # time handler

try:
  AlgorithmII()
except Exception as exc: 
  print(exc)

signal.alarm(0)




















