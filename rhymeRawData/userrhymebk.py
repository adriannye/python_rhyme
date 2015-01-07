




"""
userrhyme.py -- get user input, return rhyme list
using dicts for word-to-word info and word-to-rhyme list
"""
import sys
from pickleit import *
#from google.appengine.ext import db
from wordinfo import WordInfo

posdict = {"N": "Noun",
"p"	:"Plural",		
"h"	:"Noun Phrase",		
"V"	:"Verb (usually participle)",	
"t"	:"Verb (transitive)"	,
"i"	:"Verb (intransitive)",  	
"A"	:"Adjective"	,	
"v"	:"Adverb"	,		
"C"	:"Conjunction"	,	
"P"	:"Preposition"	,	
"!"	:"Interjection"	,	
"r"	:"Pronoun"	,		
"D"	:"Definite Article",	
"I"	:"Indefinite Article"	,
"o"	:"Nominative"}

cons_examples = \
"B ":"be",
"CH":"cheese",
"D ":"dee",
"DH":"thee",
"F ":"fee",
"G ":"green",
"HH":"he",
"JH":"gee",
"K ":"key",
"L ":"lee",
"M ":"me",
"N ":"knee",
"NG":"ping",
"P ":"pee",
"R ":"read",
"S ":"sea",
"SH":"she",
"T ":"tea",
"TH":"theta",
"V ":"vee",
"W ":"we",
"Y ":"yield",
"Z ":"zee",
"ZH":"seizure",

cons_family = \
"B ":"voiced plosive",
"CH":"unvoiced fricative",
"D ":"voiced plosive",
"DH":"voiced fricative",
"F ":"unvoiced fricative",
"G ":"voiced plosive",
"HH":"unique",
"JH":"voiced fricative",
"K ":"unvoiced plosive",
"L ":"unique",
"M ":"nasal",
"N ":"nasal",
"NG":"nasal",
"P ":"unvoiced plosive",
"R ":"unique",
"S ":"unvoiced fricative",
"SH":"unvoiced fricative",
"T ":"unvoiced plosive",
"TH":"unvoiced fricative",
"V ":"voiced fricative",
"W ":"unique",
"Y ":"unique",
"Z ":"voiced fricative",
"ZH":"voiced fricative",

cons_family_list = \
"voiced fricative":('V ','DH','Z ','ZH','JH'),
"unvoiced fricative":('F ','TH','S ','SH','CH'),
"voiced plosive":('B ','D ','G '),
"unvoiced plosive":('P ','T ','K '),
"nasal":('M ','N ','NG'),
"unique":('HH','L ','R ','W ','Y '),

if __name__ == '__main__':
    print "opening pruned word input file"
    try:
        wordinfodict = unpickleit("prunedwordinfodict")
    except IOError, e:
        print "*** can't open pruned word data file:", e
    else:
        print "opening p2rdict input file"
        try:
            p2rdict = unpickleit("p2rdict")
        except IOError, e:
            print "*** can't open w2r data file:", e
        else:             
        # get user word to rhyme    
            while 1:
                word2rhyme = raw_input('Enter word to rhyme: ')
                # clean up input
                word2rhyme = word2rhyme.lower()
                word2rhyme = word2rhyme.strip() #remove leading and trailing spaces
                #check if word to rhyme is in dict
                word2rhyme = word2rhyme.lower()
                if word2rhyme in wordinfodict:
                    phoneme = wordinfodict[word2rhyme].rhymephonemes
                    for word in p2rdict[phoneme]:
                            if word != word2rhyme:
                                    print word

                else:
                    print "Word not found in database"
            

        #"""

