#!/usr/bin/env python3

from mip import *

m = Model(solver_name=CBC)
m.read("gurobi-p0033.lp")
m.optimize()
print(m.objective_value)
for v in m.vars:
    print(v.name, v.x)

# C157 1
# C158 0
# C159 0
# C160 0
# C161 0
# C162 1
# C163 0
# C164 0
# C165 0
# C166 0
# C167 1
# C168 0
# C169 0
# C170 0
# C171 0
# C172 1
# C173 1
# C174 0
# C175 1
# C176 1
# C177 0
# C178 0
# C179 1
# C180 0
# C181 1
# C182 1
# C183 1
# C184 1
# C185 1
# C186 0
# C187 1
# C188 1
# C189 1
# Constant 1.0