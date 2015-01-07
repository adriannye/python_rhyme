
"""
userrhyme.py -- get user input, return rhyme list
using dicts for word-to-phonemeseq info and phonemeseq-to-rhyme list
"""
import sys
#from google.appengine.ext import db
from tables import *
from mytools import *


if __name__ == '__main__':
    print "opening pruned word input file"
    try:
        prunedwordinfodict = unpickleit("prunedwordinfodict")
    except IOError, e:
        print "*** can't open word info dict:", e
    else:
        print "opening p2rdict input file"
        try:
            p2rdict = unpickleit("p2rdict")
        except IOError, e:
            print "*** can't open phoneme to rhyme dict:", e
        else:             
        # get user word to rhyme    
            while 1:
                perfectrhymelist = []
                familyrhymelist = [] # will append as we generate imperfect rhymes
                additive_rhymelist = [] # will append as we generate imperfect rhymes
                subtractive_rhymelist = [] # will append as we generate imperfect rhymes
              
                word2rhyme = raw_input('Enter word to rhyme: ')
                # clean up input

                word2rhyme = word2rhyme.strip() #remove leading and trailing spaces
                #check if word to rhyme is in dict
                word2rhyme = word2rhyme.lower()
                if word2rhyme in prunedwordinfodict:
                    phonemeseq = prunedwordinfodict[word2rhyme].rhymephonemes
                    for word in p2rdict[phonemeseq]:
                        if word != word2rhyme:
                              perfectrhymelist.append(word)

                    # first loop through find consonants
                    consecutive, consonant_indexes = find_consonants(phonemeseq)

                    # for each consonant, try replacements
                    if consonant_indexes == []: #no consonants, so no family rhymes possible
                        # try additive rhyme
                        # first add s 
                        # second add plosive, voiced first
                        # then add fricatives
                        newseq = add_cons(phonemeseq, "Z")
                        index = len(newseq)-1   #last char is len-1
                        
                        try_rhymes(p2rdict, newseq, index, "Z", "Additive", additive_rhymelist)
                        # now try fricatives
                        newseq = replace_cons(newseq, index, "B") 
                        make_rhyme(p2rdict, newseq, index, "Additive", additive_rhymelist)
                       
                        newseq = replace_cons(newseq, index, "V") 
                        make_rhyme(p2rdict, newseq, index, "Additive", additive_rhymelist)
                        
                        newseq = replace_cons(newseq, index, "N") 
                        make_rhyme(p2rdict, newseq, index, "Additive", additive_rhymelist)
                    else:
                        make_rhymes(p2rdict, phonemeseq, consonant_indexes, "Family", familyrhymelist) # adds to familyrhymelist
                     
                        # if two consonants in a row, try eliminating one of the consonants,
                        # and then try replacing each of the remaining cons with a family cons
                        if consecutive != -1:
                            print consonant_indexes
                            for index in consonant_indexes:
                                if index < consecutive:
                                    continue
                                print index
                                print phonemeseq
                                print consecutive
                                newphoneseq = remove_cons(phonemeseq, consecutive)
                                print "new is", newphoneseq
                                consecutive += 1
                                throwaway, consonant_indexes = find_consonants(newphoneseq)
                                make_rhymes(p2rdict, newphoneseq, consonant_indexes, "Subtractive", subtractive_rhymelist)
                    print "perfect rhymes", perfectrhymelist
                    print "family rhymes", familyrhymelist
                    print "additive rhymes", additive_rhymelist
                    print "subtractive rhymes", subtractive_rhymelist
                else:
                    print "Word not found in database"
            
                    
        #"""

