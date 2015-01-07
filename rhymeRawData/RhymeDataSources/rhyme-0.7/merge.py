#!/usr/bin/python

import sys
import string

#This program merges two cmudict files to the stdout
#for use by makedbs in generating the text database files.
#It's the same sort of merge that mergesort uses..no biggie

file1 = open(sys.argv[1])
file2 = open(sys.argv[2])

line1 = file1.readline()
line2 = file2.readline()

try:
    while (line1 and line2):
        while ((string.strip(line1) == '') or (line1[0] == '#')):
            line1 = file1.readline()
        while ((string.strip(line2) == '') or (line2[0] == '#')):
            line2 = file2.readline()
        
        if (line1 > line2):
            sys.stdout.write(line2)
            line2 = file2.readline()
        elif (line1 < line2):
            sys.stdout.write(line1)
            line1 = file1.readline()
        else:
            #this shouldn't happen, but just in case
            sys.stdout.write(line1)
            line1 = file1.readline()
            line2 = file2.readline()

    #only one of the next two should actually execute
    while (line1):
        sys.stdout.write(line1)
        line1 = file1.readline()
    while (line2):
        sys.stdout.write(line2)
        line2 = file2.readline()
finally:
    file1.close()
    file2.close()
