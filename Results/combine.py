#!/usr/bin/python

import os, re, sys
from subprocess import *
import shutil

mmapbench_file=sys.argv[1]
malloc_file=sys.argv[2]
output_file=sys.argv[3]

mmapfile = open(mmapbench_file,'r')
mallocfile = open(malloc_file,'r')
outputfile = open(output_file,'w')

mallocValues = []

for line in mallocfile:
  if (re.search("malloc",line)):
    mallocValues.append(line)

print "Number of Malloc Entries Found Are "+str(len(mallocValues))
count=0
for line in mmapfile:
  if (re.search("malloc",line)):
    outputfile.write(mallocValues[count])
    count=count+1
  else:
    outputfile.write(line)

if (count != len(mallocValues)):
  print "Error!!!!! Number of entries written are not equal to the number of entries found in malloc csv"

mmapfile.close()
mallocfile.close()
outputfile.close()

