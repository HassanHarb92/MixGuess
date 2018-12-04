#!/usr/bin/python

#######################################################################################################################
#
#  MixGuess  v. 1.0
#  By Hassan Harb
#
#  Script that reads in MO Coefficients from two different states and creates a new checkpoint file with alpha MOs of
#  the first chkpt and beta MOs of the second chkpt
#
#  usage: python MixGuess.py Job1.fchk Job2.fchk
#
#
#  Last edited by Hassan Harb, Decemnber 3, 2018
#
#######################################################################################################################

from __future__ import division
import sys
import math
import numpy as np
from numpy import genfromtxt
import csv
from decimal import Decimal

#Function: convert output to scientific notation
def sci_notation(n):
#    n = np.real(n)
    a = '%.8E' % n
    return '%.8E' % np.real(n)


# Part 1: Read the names of the checkpoint files from the command line

NBasis = 0 
filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = "Modified-"+filename1

print "MixGuess: Generate a new guess based on MOs from two different jobs.\n"
print "Alpha MO Coefficients will be extracted from: ", filename1
print "Beta MO Coefficients will be extracted from: ", filename2
print "New MO Coefficients will be written to: ", filename3

# Part 2: Read the Alpha MO Coefficients from the first chkpt file

with open(filename1, 'r') as origin:
   for line in origin:
      if "Number of basis functions" in line:
         words = line.split()
         for i in words:
	    for letter in i:
               if(letter.isdigit()):
                  NBasis = NBasis*10 + int(letter)

print "Number of Basis Functions = ", NBasis, "\n"

NBasis2=0
with open(filename2, 'r') as origin:
   for line in origin:
      if "Number of basis functions" in line:
         words = line.split()
         for i in words:
	    for letter in i:
               if(letter.isdigit()):
                  NBasis2 = NBasis2*10 + int(letter)

if (NBasis != NBasis2): 
    print "ERROR: Files have different numbers of basis functions"
    exit()

MOElements = NBasis * NBasis
print "The code will look for  ", MOElements, " elements of the MO coefficient matrices\n"

MOlines = int(MOElements/5) + 1

if (MOElements % 5 ==0):
   MOlines = int(MOElements/5)

print "MO lines = ", MOlines, "\n"

MORawAlpha = np.zeros(MOElements)
MORawBeta = np.zeros(MOElements)

p = 0
r = 0
AOE = 0
AMO = 0
with open(filename1,'r') as origin:
    for i, line  in enumerate(origin):
        if  "Alpha MO coefficients" in line:              
              i=i+1
              AMO=i
              print "Alpha MO coefficients starts at line :", i
              AMO = i
              j=i+MOlines-1
              print "Alpha MO coefficients ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawAlpha[r] = nextline[p]
                   r = r+1
                 p = 0

# Part 3: Read the Beta MO Coefficients from the second chkpt file

p = 0
r = 0
BMO = 0
with open(filename2,'r') as origin:
    for i, line  in enumerate(origin):
        if  "Beta MO coefficients" in line:              
              i=i+1
              BMO=i
              print "Beta MO coefficients starts at line :", i
              BMO = i
              j=i+MOlines-1
              print "Beta MO coefficients ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawBeta[r] = nextline[p]
                   r = r+1
                 p = 0

print "Stored Alpha MO Coefficients = \n", MORawAlpha
print "Stored Beta MO Coefficients = \n", MORawBeta

CAlpha = np.zeros((NBasis,NBasis))
CBeta = np.zeros((NBasis,NBasis))

t=0
for i in range(0,NBasis):
   for j in range(0,NBasis):
     CAlpha[j,i]=MORawAlpha[t]
     CBeta[j,i]=MORawBeta[t]
     t=t+1


print "Alpha MO Coefficient Matrix = \n", CAlpha
print "Beta MO Coefficient Matrix = \n", CBeta

# Part 4: Write in the new matrices to a new chkpt file

print "Alpha MO placeholder = ", AMO
print "Beta MO placeholder = ", BMO 


## Part 4a : copy the first part of chkpt1, up until AMO

pointer = 0
counter = 1

with open(filename1,'r') as origin:
   data = origin.readlines()
   with open(filename3,'w') as f2:
       print "Writing results to new output file: ", filename3, "..."

       while (pointer < AMO):
          f2.write(data[pointer])
          pointer = pointer + 1

## Part 4b : write in CAlpha
       
#       f2.write(data[AMO])
       for i in range(0,NBasis):
             for j in range(0,NBasis):
                  f2.write(" ")
                  if (CAlpha[j,i] >= 0):
                     f2.write(" ")
                  f2.write(str(sci_notation(CAlpha[j,i])))
                  if (counter%5 ==0):
                      f2.write("\n")
                      counter=0
                  counter = counter + 1
           #  counter = 1
       counter = 1
       f2.write("\n")
## Part 4c : write in CBetai
       pointer = BMO - 1
       f2.write(data[pointer])

       for i in range(0,NBasis):
             for j in range(0,NBasis):
                  f2.write(" ")
                  if (CBeta[j,i] >= 0):
                     f2.write(" ")
                  f2.write(str(sci_notation(CBeta[j,i])))
                  if (counter%5 ==0):
                      f2.write("\n")
                      counter=0
                  counter = counter + 1
           #  counter = 1
       counter = 1
       f2.write("\n")

## Part 4d : copy the remaining of chkpt1 starting after BMO


       pointer = BMO + (int(NBasis*NBasis/5))+2 -1
       while (pointer < len(data)):
          f2.write(data[pointer])
          pointer = pointer+1









