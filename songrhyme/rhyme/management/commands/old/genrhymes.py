
"""
genrhymes.py -- generate rhyme lists
"""
import sys
from pickleit import *
#from google.appengine.ext import db


workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

#vowelsounds = ["-", "i", "A", "&", "@", "I", "u", "eI", "E", ]

if __name__ == '__main__':
    print "Stage 3: reading pruned word dict"
    try:
        word2phonemeseqdict = unpickleit("word2phonemeseqdict")
        commonwordlist = unpickleit("commonwordlist")
    except IOError, e:
        print "*** can't open pruned word or common word data file:", e
    else:
        print "generating rhymes"
        phonemeseqdict = {}
        phonemelist = []
        # set keys for rhyme list dictionary: key is rhyme phoneme sequence, value later will be list of wordinfo
        # first interate through words list and generate list of unique rhyme phoneme sequences, set as keys
        # also make a list for use in creating the word-to-rhymephoneme dict
        p2rdict = {} # needs to exist for test (could avoid with try)
        for word in word2phonemeseqdict: # word is key in dict
            p2rdict[word2phonemeseqdict[word]] = [] # every value is an empty list at this point
            phonemeseqdict[word2phonemeseqdict[word]] = word2phonemeseqdict[word] # vals are unique p's
            
        # fill p2rdict: append each rhyme word to value for appropriate key 
        for word in word2phonemeseqdict: # now add all words in their appropriate rhyme list
            p2rdict[word2phonemeseqdict[word]].append(word)

        for seq in phonemeseqdict:
            phonemelist.append(phonemeseqdict[seq])  # make list of unique phoneme sequences

        # before we pickle, sort each rhyme list
        for phonemeseq in p2rdict:
            p2rdict[phonemeseq].sort()  #sorts in place

        # pickle phoneme sequence to rhyme list dict
        pickleit(p2rdict, "p2rdict")

        try:
            p2rdec = open((workingdir + "p2rdec.py"), 'w')
        except IOError, e:
            print "*** can't open output dec file:", e
        else:
            p2rdec.write('p2rdict = {\n')
            for seq in phonemelist:
                p2rdec.write('"%s":[' % (seq))
                for rhyme in p2rdict[seq]:
                    p2rdec.write('"%s",' % (rhyme))
                p2rdec.write('],\n' )
            p2rdec.write('}\n')
            p2rdec.close()
