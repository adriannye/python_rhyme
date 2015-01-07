
"""
addendings.py - read big word info file and cut word file,
add trial endings to each word in big list and see if result is in cut words, 
then generate new pron file from the words in common. 
	bigwordinfodict - input
	cutwordfile - input
	wordgenpron - output
"""
import sys
from pickleit import *
from wordinfo import WordInfo

def addifvalid(origword, genword, phoneme): #adds word to dict if found in wordlist
    print "trying %s" % genword
    if genword in cutworddict:   #get pron from big dict, add suffix, add as value to cut word dict
        pron = "/".join(wordinfodict[origword].phonemes)
        print "%s: pron is %s then %s" % (genword,  pron, phoneme)
        cutworddict[genword] = pron + phoneme
        global count
        count +=1
        return True
    else:
        return False

def add_ed(word):
    addifvalid(word, word + "ed", "/i/d")

def add_d(word):
    addifvalid(word, word + "d", "/d")

def add_ing(word):
    addifvalid(word, word + "ing", "I/N/")

def add_double_cons_and_ing(word):
    x = word[-1]
    x = word + x  #double last char
    addifvalid(word, x + "ing", "I/N/")
def delete_vowel_add_ing(word):
    x = word[:-1] #delete last char
    addifvalid(word, x + "ing", "I/N/")

def add_ly(word):
    addifvalid(word, word + "ly", "/l/i")
def change_le_ly(word):
    x = word[:-1] #delete last char
    addifvalid(word, x + "ly", "/l/i")
def add_ally(word):
    addifvalid(word, word + "ally", "/l/i")

def add_er(word):
    addifvalid(word, word + "er", "/@/r")
def add_r(word):
    addifvalid(word, word + "r", "/@/r")
def add_ier(word):
    x = word[:-1] #delete last char (trailing y)
    addifvalid(word, x + "ier", "/@/r")

def add_est(word):
    addifvalid(word, word + "est", "/E/st")
def add_st(word):
    addifvalid(word, word + "st", "/E/st")
def add_iest(word):
    x = word[:-1] #delete last char (trailing y)
    addifvalid(word, x + "iest", "/E/st")
                
workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

if __name__ == '__main__':
    # attempt to open file for reading
    print "reading big word dict"
    try:
        wordinfodict = unpickleit("bigwordinfodict")
    except IOError, e:
        print "*** can't open big word data file:", e
    else:
        print "reading word list"
        try:
            wordlistfile = open((workingdir + "cutwordlist"), 'r')
        except IOError, e:
            print "*** can't open word list file:", e
        else:
        # process lines in file
            cutworddict = {}
            cutwordlist = []
            for word in wordlistfile: # parse eachLine,
                if word == "\n":
                    continue   # ignore blank lines if any

                word = word.rstrip() # delete trailing whitespace and/or newline

                cutwordlist.append(word)
                cutworddict[word] = []

            wordlistfile.close()

            print cutworddict
            count = 0
            for word in wordinfodict:
                # now add endings to word and add those to dict as well if in wordlist

                add_ed(word)
                add_d(word)

                add_ing(word)
                add_double_cons_and_ing(word)
                delete_vowel_add_ing(word)

                add_ly(word)
                change_le_ly(word)
                add_ally(word)

                add_er(word)
                add_r(word)
                add_ier(word)

                add_est(word)
                add_st(word)
                add_iest(word)
 
            print "words in common: %d" % count
            print "saving wordgenpron file"
            
            try:
                wordgenpronfile = open((workingdir + "wordgenpron"), 'w')
            except IOError, e:
                print "*** can't open word get pron file:", e
            else:
                for word in cutworddict:
                    if cutworddict[word]: #if no value, no suffix found
                        wordgenpronfile.write(word + " " + cutworddict[word] + "\n")
                wordgenpronfile.close()

