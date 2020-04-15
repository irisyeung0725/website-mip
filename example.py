
import glpk
import os
# from pulp import *
# print("starting...")
# example = glpk.glpk("example.mod")
# example.update()
# example.solve()
# print("solution:", example.solution())
# print("solution is also here: x =", example.x, "y =", example.y)
lp = glpk.LPX()  
lp.name = "sample"     # Assign symbolic name to problem
lp.obj.maximize = True # Set this as a maximization problem
lp.rows.add(3)         # Append three rows to this instance
# for r in lp.rows:      # Iterate over all rows
# 	r.name = chr(ord('p')+r.index) # Name them p, q, and r
# equal to
# lp.rows[0].name = 'p'
# lp.rows[1].name = 'q'
# lp.rows[2].name = 'r'

lp.rows[0].name = 'c1'
lp.rows[1].name = 'c2'
lp.rows[2].name = 'c3'

lp.rows[0].bounds = None, 4.0 # Set bound -inf < c1 <= 100
lp.rows[1].bounds = 1.0, None  # Set bound -inf < c2 <= 600
lp.rows[-1].bounds = None, 2.0  # Set bound -inf < c3 <= 300
# print("lp.rows=", lp.rows[0])

lp.cols.add(3)         # Append three columns to this instance
# for c in lp.cols:      # Iterate over all columns
# 	c.name = 'x' % c.index # Name them x0, x1, and x2
# 	c.bounds = 0.0, None     # Set bound 0 <= xi < inf

lp.cols[0].name = "x"
lp.cols[1].name = "y"
lp.cols[2].name = "z"

for c in lp.cols:  
    c.bounds = None, None

# make all struct variables binary
for col in lp.cols:
    col.kind = bool

# lp.obj[:] = [ 1.0, 1.0, 2.0]   # Set objective coefficients
# lp.obj.shift = 0.5
lp.obj[:] = [ 1.0 ,1.0, 2.0]
# lp.obj[:] = [ 2.0, 1.0, 2.0]    # Set objective coefficients
lp.matrix = [ 1.0, 2.0, 3.0,     # Set nonzero entries of the
             1.0, 0.0, 0.0,
             2.0, 1.0, 1.0]     #   constraint matrix.  (In this
                                   #   case, all are non-zero.)

# lp = glpk.LPX(cpxlp="/Users/cassie/Dropbox/GA/Website/example.lp")
lp.integer(presolve=True,tm_lim=30000)


# # lp.obj[:] = [ 1.0 ,0.0, 2.0]

# # lp.simplex()  
# # write file into lp format
lp.write(cpxlp="example.lp") # lpx_write_cpxlp

print('Obj_val = %g;' % lp.obj.value)  # Retrieve and print obj func value
print('; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols))
                       # Print struct variable names and primal values
print(type(lp.cols[0].bounds[0]))
print(lp.cols[1].value)
print(lp.cols[1].primal)

# print(lp.cols[0])
# # print(str(lp.cols[0].kind) == '<class ''bool''>')
# print(lp.cols[0].kind == bool)
# print(lp.nint) # get number of integer columns
# print(lp.status) # get the stauts of the model
# print(lp.obj.value) # get the object value 
# print(lp.obj.maximize == 1) # check sense
# print(lp.cols[0].primal) # get variable value
# print(lp.cols[0].name) # get variable name
# print(lp.obj[0]) # get coefficient
# print(lp.matrix)
# print(lp.rows[1].matrix)
# print(lp.rows[1].matrix == len(lp.cols))
# mylist= [None] * len(lp.cols)
# # mylist[0] = 2
# # print(mylist)
# for i in range(len(lp.rows[1].matrix)):
#     index = lp.rows[1].matrix[i][0]
#     value = lp.rows[1].matrix[i][1]
#     if lp.rows[1].matrix != len(lp.cols):
#         diff = len(lp.cols) - len(lp.rows[1].matrix)
#         mylist[index] = value


# # another_lp = lp
# # another_lp.obj[:] = [1.0,1.0,2.0]
# # print(lp.obj[0], another_lp.obj[0])
# # print(another_lp.matrix)
# # print(len(another_lp.rows))
# # another_lp.rows.add(1)
# # print(len(another_lp.rows))

# # another_lp.rows[len(another_lp.rows)-1].name = 'c3'
# # print(type(another_lp.matrix[0]))
# # row_coeff = [2.0, 3.0, 4.0]
# # another_lp.rows[2].bounds = 1.0, None
# # row_tuple = ()
# # for i in row_coeff:
# #     row_tuple.append(i)
# # another_lp.matrix.append(row_coeff)
# # print(another_lp.matrix)
# # a = (1, 2, 3.0)
# # # b = another_lp.matrix
# # # b.append(a)
# # print(another_lp.matrix)
# # b= [(0, 0, 1.0), (0, 1, 2.0), (0, 2, 3.0), (1, 0, 1.0), (1, 1, 1.0)]
# # b.append(a)
# # mat = []
# # for tup in another_lp.matrix:
# #     mat.append(tup[2])
# # print(mat)
# # print(len(another_lp.rows[0].matrix))
# # print(len(another_lp.cols))
# # for i in range(len(another_lp.matrix)):
# #     if len(another_lp.rows[i].matrix)) == len(another_lp.cols)
    

# # b.append(a)
# # print(b)
# # another_lp.rows)-1,
# # print(lp.rows)
# # print(help(glpk))
# # col = [0] * lp.nint
# # print(col)
# # for i in col:
# #     del(lp.cols[i])


# # del(lp.cols[0])
# # print('; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols))
#                        # Print struct variable names and primal values
# # print(lp.cols[0].name)
# # print(lp.rows[0].name)


# # file_path = "/Users/cassie/Dropbox/GA/Website/example.lp"
# # file_name = file_path.split("/")[-1]
# # input_file_name = os.path.basename(file_path)
# # print(input_file_name)
# # print(lp.status)
# # del(lp.cols[0,1,2])

# import numpy as np
# # given = np.array([(0,0,1),(0,1,1),(1,0,1),(1,2,2)])
# # print("Given:")
# # print(given)
# # maxvar = np.max(given[:,1])
# # maxeq = np.max(given[:,0])
# # print(maxvar, maxeq)
# # res = np.zeros((maxeq+1,maxvar+1))
# # print("\nPlaceholder:")
# # print(res)
# # for rn in range(len(given)):
# #     for cn in range(len(given[rn])-1):
# #             res[given[rn,0],given[rn,1]] = given[rn, 2]
# # print(given[rn,0], given[rn,1])
# # print(res[1,2])

# # print("\nResult:")
# # print(res)
# # print(type(given[0]))
# # print(np.ravel(res))
# matrix = np.array(lp.matrix)
# print('matrix', matrix)
# # print(type(matrix[0]))

# num_of_var = lp.nint
# num_of_row = len(lp.rows)
# len_matrix = len(matrix)
# print(len_matrix)
# mat = np.zeros((num_of_var,num_of_row))
# print(mat)
# # print(res)
# # for rn in range(len(matrix)):
# #     for cn in range(len(matrix)-1):
# #         res[matrix[rn,0],matrix[rn,1]] = matrix[rn,2]
# # print(res)
# print('rows:', len(lp.rows))
# print('vars:', lp.nint)
# print(type(lp.nint))
# print(type(len(lp.rows)))
# for i in range(len_matrix):
#     print(i)
#     for j in range(len(matrix)-1):
#         mat[int(matrix[i,0]),int(matrix[i,1])] = matrix[i,2]
#         # print(int(matrix[i,0]),int(matrix[i,1]),matrix[i,2])

# mat = list(np.ravel(mat))
# print(mat)
# print(lp.rows[-1].matrix)
# from pulp import *

# a = solvers.GLPK("/Users/cassie/Dropbox/GA/Website/example.lp",1)
# a.solve()
