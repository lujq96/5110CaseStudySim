# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 19:04:48 2018

@author: lujq9
"""

import csv
import random
import math

with open('demand.csv', 'r') as f:
    demand = list(csv.reader(f, delimiter=','))
demand = [r[:7] for r in demand]
for r in range(1, len(demand)):
    for c in range(len(demand[0])):
        demand[r][c] = float(demand[r][c])
demand[0][0] = 'Weeks'
for r in range(1, len(demand)):
    demand[r][0] = 51 - demand[r][0]

tilt = [None, 0.09719, 0, 0.05830, 0, -0.07457, 0]

print(demand[:3])

residual = demand[:]

for r in range(1, len(demand)):
    for c in range(1, len(residual[0])):
        residual[r][c] = residual[r][c] - residual[r][0]*tilt[c]

def demand_gen(t=1, n99=False, history=False):
    """Generate future demand w/ linear model."""
    if history:
        assert t >= 1 and t <= 50, "t is out of range for historical data."
        assert n99 == False, "No N99 in historical data."
        return [r[1:] for r in demand if r[0] == t][0]
    t += 50
    vector = list()
    for c in range(1, len(residual[0])):
        c_residual = [r[c] for r in residual[1:]]
        c_predict = max(math.ceil(t*tilt[c] + random.choice(c_residual)), 0)
        vector.append(c_predict)
    if n99:    
        vector.append(random.choice(range(2,7)))
    return vector