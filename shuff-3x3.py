#!/usr/bin/env python
import random, sys

one   = []
two   = []
three = []

rng = range(12)
if len(sys.argv) > 1:
  rng = range(6, 12)
for i in rng:
  one.append("$$%d" % ((i*3)+1))
  two.append("$$%d" % ((i*3)+2))
  three.append("$$%d" % ((i*3)+3))
  
r = range(6)
random.shuffle(r)
r1 = r[:3]
r2 = r[3:]

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % one[r1[i]])
sys.stdout.write(",")

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % two[r1[i]])
sys.stdout.write(",")

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % three[r1[i]])
sys.stdout.write(",")

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % one[r2[i]])
sys.stdout.write(",")

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % two[r2[i]])
sys.stdout.write(",")

for i in range(3):
  if i > 0:
    sys.stdout.write("+")
  sys.stdout.write("%s" % three[r2[i]])
print ""
