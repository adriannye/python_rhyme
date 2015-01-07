
"""
pickleit.py -- utility functions to pickle and unpickle
"""
import sys
import pickle
import marshal

workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

def pickleit(data, filename):
        # attempt to open file for writing
    try:
        fobj = open(workingdir + filename, 'wb')
    except IOError, e:
        print "*** can't open output file %s:", filename, e
    else:
        pickle.dump(data, fobj, 2)
        fobj.close()

def unpickleit(filename):
        # attempt to open file for reading
    try:
        fobj = open(workingdir + filename, 'rb')
    except IOError, e:
        print "*** can't open input file %s:", filename, e
    else:
        data = pickle.load(fobj)
        fobj.close()
        return data

def marshalit(data, filename):
        # attempt to open file for writing
    try:
        fobj = open(workingdir + filename, 'wb')
    except IOError, e:
        print "*** can't open output file %s:", filename, e
    else:
        marshal.dump(data, fobj)
        fobj.close()

def unmarshalit(filename):
        # attempt to open file for reading
    try:
        fobj = open(workingdir + filename, 'rb')
    except IOError, e:
        print "*** can't open input file %s:", filename, e
    else:
        data = marshal.load(fobj)
        fobj.close()
        return data
