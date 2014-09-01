#!/usr/bin/env python3

# Generates a matrix1 file
import sys, math, numpy
from pyDOE import pbdesign;
from scipy import linalg

if (len(sys.argv) < 2):
    print("USAGE: genmat.py <factor count>")
    sys.exit()

# Get the number of factors.
n = int(sys.argv[1])

# Get the nearest N
#N = math.ceil(int(n) / 4) * 4

# Generate design
try:
    mat = pbdesign(n)
except:
    # Fallback to hadamard
    mat = linalg.hadamard(n, numpy.float64)

# Format the matrix
for idx, row in enumerate(mat):
    print("{} {}".format(idx, (' {: 1.0f} '*n).format(*row)))
