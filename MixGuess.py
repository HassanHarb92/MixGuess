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
flag = sys.argv[3]

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

MORawAlpha1 = np.zeros(MOElements)
MORawBeta1 = np.zeros(MOElements)
MORawAlpha2 = np.zeros(MOElements)
MORawBeta2 = np.zeros(MOElements)

p = 0
r = 0
AMO1 = 0
BMO1 = 0
with open(filename1,'r') as origin:
    for i, line  in enumerate(origin):
        if  "Alpha MO coefficients" in line:              
              i=i+1
              AMO1=i
              print "Alpha MO coefficients starts at line :", i
              AMO1 = i
              j=i+MOlines-1
              print "Alpha MO coefficients ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawAlpha1[r] = nextline[p]
                   r = r+1
                 p = 0

        p = 0
        r = 0
        if  "Beta MO coefficients" in line:
              i=i+1
              BMO1=i
              print "Beta MO coefficients in file 1 starts at line :", i
              BMO1 = i
              j=i+MOlines-1
              print "Beta MO coefficients in file 1  ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawBeta1[r] = nextline[p]
                   r = r+1
                 p = 0

# Part 3: Read the Beta MO Coefficients from the second chkpt file

p = 0
r = 0
AMO2 = 0
BMO2 = 0
with open(filename2,'r') as origin:
    for i, line  in enumerate(origin):
        if  "Alpha MO coefficients" in line:
              i=i+1
              AMO2=i
              print "Beta MO coefficients starts at line :", i
              AMO2 = i
              j=i+MOlines-1
              print "Beta MO coefficients ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawAlpha2[r] = nextline[p]
                   r = r+1
                 p = 0
        r = 0
        p = 0
        if  "Beta MO coefficients" in line:              
              i=i+1
              BMO2=i
              print "Beta MO coefficients starts at line :", i
              BMO2 = i
              j=i+MOlines-1
              print "Beta MO coefficients ends at line :", j
              for m in range(0,j-i+1):
                 nextline = origin.next()
                 nextline = nextline.split()
                 for p in range(p,len(nextline)):
                   MORawBeta2[r] = nextline[p]
                   r = r+1
                 p = 0

print "Stored Alpha MO Coefficients from chkpt1 = \n", MORawAlpha1
print "Stored Beta MO Coefficients from chkpt1 = \n", MORawBeta1

print "Stored Alpha MO Coefficients from chkpt2 = \n", MORawAlpha2
print "Stored Beta MO Coefficients from chkpt2 = \n", MORawBeta2

CAlpha = np.zeros((NBasis,NBasis))
CBeta = np.zeros((NBasis,NBasis))


######## ADD ALL FOUR IF STATEMENTS: 1 (A,A), 2(A,B), 3(B,A), 4(B,B)

if (flag == "aa"):
    print "Copying Alpha MO (chkpt1)  -> Alpha MO (chkpt3)\n"
    print "Copying Alpha MO (chkpt2) -> Beta MO (chkpt3)\n"
    t=0
    for i in range(0,NBasis):
       for j in range(0,NBasis):
         CAlpha[j,i]=MORawAlpha1[t]
         CBeta[j,i]=MORawAlpha2[t]
         t=t+1

elif (flag == "ab"):
    print "Copying Alpha MO (chkpt1)  -> Alpha MO (chkpt3)\n"
    print "Copying Alpha MO (chkpt2) -> Beta MO (chkpt3)\n"
    t=0
    for i in range(0,NBasis):
       for j in range(0,NBasis):
         CAlpha[j,i]=MORawAlpha1[t]
         CBeta[j,i]=MORawBeta2[t]
         t=t+1

if (flag == "ba"):
    print "Copying Alpha MO (chkpt1)  -> Alpha MO (chkpt3)\n"
    print "Copying Alpha MO (chkpt2) -> Beta MO (chkpt3)\n"
    t=0
    for i in range(0,NBasis):
       for j in range(0,NBasis):
         CAlpha[j,i]=MORawBeta1[t]
         CBeta[j,i]=MORawAlpha2[t]
         t=t+1

if (flag == "bb"):
    print "Copying Alpha MO (chkpt1)  -> Alpha MO (chkpt3)\n"
    print "Copying Alpha MO (chkpt2) -> Beta MO (chkpt3)\n"
    t=0
    for i in range(0,NBasis):
       for j in range(0,NBasis):
         CAlpha[j,i]=MORawBeta1[t]
         CBeta[j,i]=MORawBeta2[t]
         t=t+1

###################################################################

print "Alpha MO Coefficient Matrix to be copied to chkpt3 = \n", CAlpha
print "Beta MO Coefficient Matrix to be copied to chkpt3 = \n", CBeta

# Part 4: Write in the new matrices to a new chkpt file

AMO = AMO1
BMO = BMO2

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
       pointer = BMO 
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


       pointer = BMO + (int(NBasis*NBasis/5))+2
       while (pointer < len(data)):
          f2.write(data[pointer])
          pointer = pointer+1


print "Writing results to new output file...  COMPLETE"
