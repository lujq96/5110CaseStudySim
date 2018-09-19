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
x0 = [None, 2.48163, 0, 1.47347, 0, 7.40163, 0]

residual = [sub[:] for sub in demand]

for r in range(1, len(demand)):
    for c in range(1, len(residual[0])):
        residual[r][c] = residual[r][c] - (residual[r][0]*tilt[c] + x0[c])

def demand_gen(t=1, n99=False):
    """Generate future demand w/ linear model."""
    t += 50
    vector = list()
    for c in range(1, len(residual[0])):
        c_residual = [r[c] for r in residual[1:]]
        c_predict = max(math.ceil(x0[c] + t*tilt[c] + random.choice(c_residual)), 0)
        vector.append(c_predict)
    if n99:    
        vector.append(random.choice(range(2,7)))
    return vector

#random.choice([r[5] for r in residual[1:]])
# Output demand projection as csv
def fut_demands(t0=1, tn=1, n99=False):
    """Use demand_gen to generate future demand from week t0 to tn."""
    output = [[e for e in demand[0]]]
    if n99:
        output[0].append('N99')
    for t in range(t0, tn + 1):
        pred = [t] + demand_gen(t, n99)
        output.append(pred)
    return output

future_demand_16 = fut_demands(1, 16)
future_demand_50 = fut_demands(1, 50)

# Export csv
def export_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        demandwriter = csv.writer(csvfile, dialect='excel')
        for r in range(len(data)):
            demandwriter.writerow(data[r])
if __name__=='__main__':
	export_csv("future_demand_16.csv", future_demand_16)
	export_csv("future_demand_50.csv", future_demand_50)