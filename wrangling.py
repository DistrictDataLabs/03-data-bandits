# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 11:31:30 2015

@author: ed
"""

import csv

with open('cpi.csv', 'rU') as f:
   data = [row for row in csv.reader(f)]

last = data[-1]
cpinum = [float(number) for number in last if number != '']
cpi = cpinum[-1]

output = open("data.txt","w")
output.write(str(cpi))
output.close()





