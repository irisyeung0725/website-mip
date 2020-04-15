from glpk import *
import sys
import time
import signal


##-- find local time
local_time = time.asctime(time.localtime(time.time()))

##-- check to see if input file and k is passed to script and load them
##-- this part is not needed because Prachi is checking
# if (len(sys.argv) < 3):
  # print('Please Enter your Input file and K')
  # quit(0)
  
input_file = sys.argv[1]
k = int(sys.argv[2])

##-- creating output file name based on input file name
output_file_path = "/Users/cassie/Dropbox/GA/Website/"
input_file_name = os.path.basename(input_file)
input_file_ext = input_file_name.split(".")[1]
output_file_name = input_file_name.split(".")[0]

##-- check if file format .lp/.mps is correct
##-- this part is not needed if Prachi is checking file format but I still check it as now I have access to output file based on input file name
# problem = glpk.LPX()
if (input_file_ext=="lp"):
  problem = glpk.LPX(cpxlp=input_file)
elif (input_file_ext=="mps"):
  problem = glpk.LPX(mps=input_file)
else:
  f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'w')
  f.write ("Local date and time is: {0} \n\n".format (local_time))
  f.write("Input file format is incorrect. only .lp/.mps formats are acceptable.")
  f.close()
  quit()

##-- initializing debug file
#debug_file_path = "//home/narges/Documents/#debug"
#debug = open ("{0}/{1}.txt".format(#debug_file_path,output_file_name), 'w')
#debug.write ("#debug File ********************************************* Local date and time is: {0} \n\n".format (local_time))

def AlgorithmII():
  ##-- define variables
  l = 0 
  X = {}
  num_binary_vars = 0
  epsilon = 1e-6
  F = float(0)
  Lambda = float(0)
  Dbin = float(0)
  do = float(2)
  Nx_value = float(0)
  Dx_value = float(0)
  Max_Dx_opt_sol = float(0)
  Max_Nx_opt_sol = float(0)

  ##--set presolving parameter
#   parm = glp_iocp()
#   glp_init_iocp(parm)
#   parm.presolve = 1
#   parm.tm_lim = 300000
  
  ##-- obtain original model direction Min OR Max (we need it for calculating quality)
  org_model_sense = problem.obj.maximize 
  if (org_model_sense == True):
	  direction = "MAXIMIZATION"
  else:
	  direction = "MINIMIZATION"
	
  ##-- sumbit the header before start optimization
  f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'w')
  f.write ("Local date and time is: {0} \n\n".format (local_time))
  f.write ("Finding {0} diverse and high-quality solutions to {1}\n".format(k,input_file_name))
  f.write ("Original model direction is {0}\n".format(direction))
  f.write ("Diversity metric is to maximize distance from centroid\n\n")
  f.write ("No(k)\tIterations\tOptObjVal\tGapOffOptimal\tDiversityMeasure\tSolution\n\n")
  f.close()

  ##-- optimize the original model
  status = problem.integer(presolve=True,tm_lim=30000) ##-- set presolving psrsmeter
  

  ##-- terminate if the original model is infeasible
  if (status != 0):
    f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
    f.write("The original model is infeasible\n\n.")
    f.close()
    quit()

  ##-- since now all we do is maximization
  problem.obj.maximize = True

  ##-- obtain number of columns/variables in original model
  number_of_vars = len(problem.cols)

  ##-- obtain number of rows in original model
  number_of_rows = len(problem.rows)

  ##-- obtain optimized value of objective function of original model
  org_opt_sol = problem.obj.value


  ##-- obtain variables kind
  ##-- GLP_CV | continuous variable
  ##-- GLP_IV | integer variable
  ##-- GLP_BV | binary variable

  ##-- obtain variables type
  ##-- GLP_FR | free (unbounded) variable
  ##-- GLP_LO | variable with lower bound
  ##-- GLP_UP | variable with upper bound
  ##-- GLP_DB | double-bounded variable
  ##-- GLP_FX | fixed variable

  var_kind = {}
#   var_type = {}
  var_lb = {}
  var_ub = {}
  for i in range(number_of_vars):
    var_kind[i] = problem.cols[i].kind
    var_lb[i] = problem.cols[i].bounds[0]
    var_ub[i] = problem.cols[i].bounds[1]
    # var_type[i] = glp_get_col_type(problem, i+1)


  ##-- find the number of binary variables
  for i in range(number_of_vars):
    X[l,i] = problem.cols[i].value
    if((opt_var[i].kind == bool or opt_var[i].kind == int) and (int(var_ub[i])==1 and int(var_lb[i]==0))):
      num_binary_vars += 1

  #debug.write("number of variables = {0}\nNumber of binaries = {1}\n".format(number_of_vars,num_binary_vars))
  #debug.write ("var_kind = {0}\nvar_type = {1}\nvar_ub = {2}\nvar_lb = {3}\n\n".format(var_kind, var_type, var_ub, var_lb))


  ##-- obtain coeficients of original model
  org_obj_coef = {}
  for i in range(number_of_vars):
    org_obj_coef[i] = problem.obj[i]
     
  #glp_write_lp(problem, None, "/home/narges/Documents/Knapsack_output.lp")


  ##-- submit original solution into output file
  f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
  f.write ("%3d\t%10d\t%10.10f\t%10.10f\t%10.10f\t" %(0,0,org_opt_sol,0,0))
  for i in range(number_of_vars):
    f.write("%.0f\t" %abs(X[l,i])) 
  f.write ("\n")
  f.close()


  ##-- build and solve Max_D(x) --> z* - Cx for maximization and Cx - z* for minimization
  Dx_coef = {}

  if (direction == "MAXIMIZATION"):
    for i in range(1 , number_of_vars+1):
      Dx_coef[i] = -1 * org_obj_coef[i]
    Dx_coef[0] = org_opt_sol
  else:
    for i in range(1 , number_of_vars+1):
      Dx_coef[i] = org_obj_coef[i]
    Dx_coef[0] = -1 * org_opt_sol    

  for i in range(number_of_vars+1):
    problem.obj[i] = Dx_coef[i]

  lp.integer(presolve=True,tm_lim=30000)

  Max_Dx_opt_sol = problem.obj.value

  Max_Dx_opt_var_val = {}
  for i in range(number_of_vars):
    Max_Dx_opt_var_val[i] = problem.cols[i].value
     
  Max_Dx_obj_coef = {}
  for i in range(number_of_vars):
    Max_Dx_obj_coef[i] = problem.obj[i]
    

  ##-- defining new variables to start while loop
  size = number_of_vars +1
  new_cnstr_var_indis = intArray(size)
  new_cnstr_coefs = doubleArray(size)
  c = {}
  x_k = {}
  s = {}
  q = {}
  DinkleBach_func_opt_var_val = {}
  Nx_coef = {}
  Max_Nx_opt_var_val = {}
  Max_Nx_obj_coef = {}
  DinkleBach_func_coef = {}

    
  #debug.write("Max Dx = {0}\n".format(Max_Dx_opt_sol))

  ##-- start while loop to find k diverse solution
  while (l < k):

  ##-- Add new constraint 
    new_cnstr_const = 0
    glp_add_rows(problem, 1)
    number_of_rows += 1     

    for i in range(number_of_vars):

      new_cnstr_var_indis[i+1] = i+1
      if ((var_kind[i] == GLP_BV or var_kind[i] == GLP_IV) and (var_ub[i]==1 and var_lb[i]==0 )):

        if (X[l,i] == 0):      
          new_cnstr_coefs[i+1] = 1
        else:
          new_cnstr_coefs[i+1] = -1
          new_cnstr_const += 1
      else:
          new_cnstr_coefs[i+1]= 0
      
    glp_set_mat_row(problem, number_of_rows, number_of_vars , new_cnstr_var_indis ,new_cnstr_coefs)  
    glp_set_row_bnds(problem, number_of_rows, GLP_LO, (1 - new_cnstr_const), 0.0)

  ##-- increase l
    l = l + 1

  ##-- calculate centroid
    for i in range(number_of_vars):
      c[i] = 0
      
    for i in range(number_of_vars):
      if ((var_kind[i] == GLP_BV or var_kind[i] == GLP_IV) and (var_ub[i]==1 and var_lb[i]==0 )):
        for j in range(l):
          c[i] += X[j,i] 
                  
        c[i] = c[i]/l
           
     
  ##-- build and solve Max_N(x)
    Nx_coef[0] = 0

    for i in range(number_of_vars):

      if ((var_kind[i] == GLP_BV or var_kind[i] == GLP_IV) and (var_ub[i]==1 and var_lb[i]==0 )):
        Nx_coef[i+1] = 1 - 2*c[i]
        Nx_coef[0] += c[i]
      else:
        Nx_coef[i+1] = 0

      glp_set_obj_coef(problem, i+1, Nx_coef[i+1])

    glp_set_obj_coef(problem, 0, Nx_coef[0])   

    status = glp_intopt(problem, parm) 

  ##-- check and terminate if new model is infeasible
    if (status != 0):
      f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
      f.write("All feasible solutions have been identified. Present model is infeasible.".format(status))
      f.close()
      quit()

    Max_Nx_opt_sol = glp_mip_obj_val(problem)
     
    for i in range(number_of_vars):
      Max_Nx_opt_var_val[i] = glp_mip_col_val(problem, i+1)

    for i in range(number_of_vars+1):
      Max_Nx_obj_coef[i] = glp_get_obj_coef(problem, i)
    

  ##-- calculate normalization factor f  
    F = Max_Dx_opt_sol / (Max_Nx_opt_sol + epsilon)
   
    #debug.write("************************************************************L = {0}\nMax Nx = {1}\nF = {2}\n".format(l,Max_Nx_opt_sol, F ))


  ##-- Identify initial solution x0 to pass into dinkelbach... I use the previouse diverse optimal solution as start point
    for i in range(number_of_vars):
      x_k[i] = X[l-1,i]    
         
    true = 1 
    counter = 0

  ##-- start dinkelbach
    while true:        
      counter += 1
          
  ##-- Calculate Nx        
      Nx_value = Nx_coef[0] 
      for i in range(number_of_vars):      
        s[i] = Nx_coef[i+1] * x_k[i]
        Nx_value = Nx_value + s[i]

  ##-- Calculate Dx  
      Dx_value = Dx_coef[0]
      for i in range(number_of_vars):     
        q[i] = Dx_coef[i+1] * x_k[i]
        Dx_value = Dx_value + q[i]
          
  ##-- Calculate Lambda  
      Lambda = F * ( Nx_value / (Dx_value + epsilon))  

      #debug.write("******************************Iteration = {0}\nNx value = {1}\nDx value = {2}\nLambda = {3}\n".format(counter,Nx_value,Dx_value,Lambda)) 

  ##-- create F*N(x) - Landa*D(x) 
      DinkleBach_func_coef[0] = (F * Nx_coef[0]) - (Lambda * (Dx_coef[0] + epsilon ))
      glp_set_obj_coef(problem, 0, DinkleBach_func_coef[0])       
            
      for i in range(number_of_vars):
        DinkleBach_func_coef[i+1] = (F * Nx_coef[i+1])  - (Lambda * Dx_coef[i+1] ) 
        glp_set_obj_coef(problem, i+1, DinkleBach_func_coef[i+1])   

  ##-- maximize F*N(x) - Landa*D(x) 
      glp_intopt(problem, parm)

  ##-- obtain max value for F*N(x) - Landa*D(x)
      DinkleBach_func_opt_sol = glp_mip_obj_val(problem)
          
  ##-- obtain arg max values for F*N(x) - Landa*D(x)
      for i in range(number_of_vars):
        DinkleBach_func_opt_var_val[i] = glp_mip_col_val(problem, i+1)
      
  ##-- check if max value for F*N(x) - Landa*D(x) == Zero 
  ##-- 
      if ( - 0.001 <= DinkleBach_func_opt_sol <= 0.001):

        #debug.write("YES  DinkelBach = {0}\n".format(DinkleBach_func_opt_sol) )     

  ##--save this new solution     
        for i in range(number_of_vars):
          X[l,i] =  DinkleBach_func_opt_var_val[i]

  ##-- calculate optimal value for this new solution (objective value of this new diverse solution)
        if (direction == "MAXIMIZATION"):
          div_opt_val = org_opt_sol - Dx_value
        else:
          div_opt_val = org_opt_sol + Dx_value

  ##-- calculate DiversityMeasure      
        Dbin_ = float(0)     
        for i in range(number_of_vars):
          if ((var_kind[i] == GLP_BV or var_kind[i] == GLP_IV) and (var_ub[i]==1 and var_lb[i]==0 )):
            for j in range(l):
              for w in range(j+1 , l+1):
                Dbin_ += abs(X[j,i]-X[w,i])
       
        Dbin = Dbin_ * do / ( num_binary_vars*(l+1)*l )

  ##-- report new solution and add findings to output file
        f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
        f.write ("%3d\t%10d\t%10.10f\t%10.10f\t%10.10f\t" %(l,counter,div_opt_val,abs(Dx_value/(epsilon+org_opt_sol)),Dbin))
        for i in range(number_of_vars):
          f.write("%.0f\t" %abs(X[l,i]))
        f.write ("\n")		
        f.close()
    
  ##-- terminate this dinkelbach and go to get initialize to find another diverse solution 		
        true = 0

  ##-- if No  F*N(x) - Landa*D(x) != Zero
      else:
  ##-- X_k <-- X_K+1 ... back to --> start dinkelbach 
        for i in range(number_of_vars):
          x_k[i] = DinkleBach_func_opt_var_val[i]

        #debug.write("NO  DinkelBach = {0}\n".format(DinkleBach_func_opt_sol) )

  ##-- if after 100 iteration it could not find a point which F*N(x) - Landa*D(x) == Zero then terminate it
  ##-- this part is not needed after putting whath dog
        #if (counter>100):
          #f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
          #f.write ("Unexpected Iteration to find the next point. Process terminated")
          #f.close()
          #quit()

  #debug.close()


def handler(signum, frame):
  f = open ("{0}/{1}.out".format(output_file_path,output_file_name), 'a+')
  f.write ("The search was prematurely terminated, because the time limit has been exceeded.")
  f.close()
  raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)
signal.alarm(300)

try:
  AlgorithmII()
except Exception, exc: 
  print(exc)

signal.alarm(0)

##-- draft
#glp_write_lp(problem, None, "//home/narges/Documents/#debug/TZ_bug_glpk{0}.lp".format(l))


