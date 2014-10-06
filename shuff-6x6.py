#!/usr/bin/env python
import random, sys

one   = []
two   = []
three = []
for i in range(12):
  one.append("$$%d" % ((i*3)+1))
  two.append("$$%d" % ((i*3)+2))
  three.append("$$%d" % ((i*3)+3))
  
r = range(12)
random.shuffle(r)
r1 = r[:6]
r2 = r[6:]

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % one[r1[i]])
sys.stdout.write(",")

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % two[r1[i]])
sys.stdout.write(",")

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % three[r1[i]])
sys.stdout.write(",")

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % one[r2[i]])
sys.stdout.write(",")

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % two[r2[i]])
sys.stdout.write(",")

for i in range(6):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % three[r2[i]])
print ""
