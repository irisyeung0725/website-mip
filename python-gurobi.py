#!/usr/bin/env python3

from gurobipy import *

input_file = "air03.mps"
m = read(input_file)

m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
print(m.modelSense)
m.modelSense = -1
m.optimize()
print('Obj: %g' % m.objVal)


