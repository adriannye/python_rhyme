
"""
2csv.py -- convert databases into csv format
"""
import sys
from pickleit import *
#from google.appengine.ext import db
#from wordinfo import WordInfo


if __name__ == '__main__':
    print "opening word to phoneme seq dict"
    try:
        w2pdict = unpickleit("w2pdict")
    except IOError, e:
        print "*** can't open word to phone dict:", e
    else:
        







        
    print "opening phoneme seq to rhyme dict"
    try:
        p2rdict = unpickleit("p2rdict")
    except IOError, e:
        print "*** can't open phoneme to rhyme dict:", e
    else:             
    # get user word to rhyme    
        while 1:
            word2rhyme = raw_input('Enter word to rhyme: ')
            # clean up input
            word2rhyme = word2rhyme.lower()
            word2rhyme = word2rhyme.strip() #remove leading and trailing spaces
            #check if word to rhyme is in dict
            word2rhyme = word2rhyme.lower()
            if word2rhyme in w2pdict:
                phoneme = w2pdict[word2rhyme]
                for word in p2rdict[phoneme]:
                        if word != word2rhyme:
                                print word

            else:
                print "Word not found in database"
        

        #"""

