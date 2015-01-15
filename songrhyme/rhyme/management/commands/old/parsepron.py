
"""
parsepron.py -- read and parse pronunciation and part of speech files,
generate dicts for word info and rhyme list
This is based on CMU pron database
"""
import sys
#import re
import pickle
workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"
from pickleit import *

#from google.appengine.ext import db

"""
wordinfo.py -- define word info class and universal utility stuff
"""

class WordInfo: # list representing all associated data for a word
    pass
    def __init__(self, phonemes=[], rhymephonemes="", pos=[]):
        self.phonemes, self.rhymephonemes, self.pos = \
                       phonemes, rhymephonemes, pos


workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

def translate_phoneme_sequence(phonemeseq):
    """
    replace two letter phonemes with a single letter special char
    """
    # slow and dirty
    phonemeseq = phonemeseq.replace("CH", '!')
    phonemeseq = phonemeseq.replace("DH", '@')
    phonemeseq = phonemeseq.replace("HH", '#')
    phonemeseq = phonemeseq.replace("JH", '$')
    phonemeseq = phonemeseq.replace("SH", '%')
    phonemeseq = phonemeseq.replace("TH", '^')
    phonemeseq = phonemeseq.replace("ZH", '&')
    phonemeseq = phonemeseq.replace("NG", '*')
    phonemeseq = phonemeseq.replace('AA','(',)
    phonemeseq = phonemeseq.replace('AE',')',)
    phonemeseq = phonemeseq.replace('AH','-',)
    phonemeseq = phonemeseq.replace('AO','_',)
    phonemeseq = phonemeseq.replace('AW','+',)
    phonemeseq = phonemeseq.replace('AY','=',)
    phonemeseq = phonemeseq.replace('EH',';',)
    phonemeseq = phonemeseq.replace('ER',':',)
    phonemeseq = phonemeseq.replace('EY','<',)
    phonemeseq = phonemeseq.replace('IH',',',)
    phonemeseq = phonemeseq.replace('IY','>',)
    phonemeseq = phonemeseq.replace('OW','.',)
    phonemeseq = phonemeseq.replace('OY','?',)
    phonemeseq = phonemeseq.replace('UH','/',)
    phonemeseq = phonemeseq.replace('UW','|')
    return phonemeseq

if __name__ == '__main__':
    #def main():
    # attempt to open file for reading
    try:
        fobj = open((workingdir + "mypronsrc.txt"), 'r')
    except IOError, e:
        print "*** can't open pronunciation data file:", e
    else:
        # process lines in file
        pos = []  #not filled in until reading POS file
        wordinfodict = {}  # dict, key is word, value is wordinfo class instance
        linecount = 0
        allphonemes = {}
        print "Stage 1:processing pron"
        for eachLine in fobj: # parse eachLine,
            # create data item for each field in WordInfo,
            # then create new WordInfo from it,
            # then add to WordList
            if eachLine == "\n":
                continue   # breaks to next input line

            substrings = eachLine.split(" ") # split into word and pronunciation (at space)
            #print substrings
            spelling = substrings[0].lower() # copy word to spelling field, initial cap
            

            phonemes = substrings[1].split("/")  # split pronunciation into 1 field per phoneme


            primstress = [] # empty list we can append to in loop
            secstress = []
            
            phonemes[-1] = phonemes[-1].rstrip() # last phoneme has return on end. strip

            # record stress and delete stress marks from phonemes
            for (i, phoneme) in enumerate(phonemes):
                if "+" in phoneme:
                    phonemes[i] = phoneme.replace("+", "")   # replace returns copy
                    primstress.append(i)   # append doesn't return copy, changes in place
                if "," in phoneme:
                    phonemes[i] = phoneme.replace(",", "")   # replace returns copy
                    secstress.append(i)   # append doesn't return copy, changes in place

                # set key in allphonemes dict to phoneme, all values empty lists
                allphonemes[phonemes[i]] = []
                
            # rhyme phonemes go from last primary stressed syllable to end of word
            # but short words don't have marked stress
            # and some other words do not have marked stress

            if len(primstress) != 0:
                rhymephonemes = "".join(phonemes[primstress[-1]:])  # concatenate the last 6 phonemes, ignore empties
            else: #short word or no stress marked
                rhymephonemes = "".join(phonemes[-6:])  # concatenate the last 6 phonemes, ignore empties
            #print "word is %s, rhymephonemes are %s" % (spelling ,rhymephonemes)
           
            #re.match('/(.*)/(.*)/(.*)', substrings[1])
            rhymephonemes = translate_phoneme_sequence(rhymephonemes)

            wordinfodict[spelling] = WordInfo(phonemes, rhymephonemes, pos)

        fobj.close()

    # add pos to wordinfodict
    try:
        fobj = open((workingdir + "Mobypossrc.txt"), 'r')
    except IOError, e:
        print "*** can't open pos data file:", e
    else:
        # process lines in file
        pos = []
        linecount = 0
        print "running pos"
        for eachLine in fobj: # parse eachLine,
            eachLine = eachLine.rstrip()
            substrings = eachLine.split("\\") # split into word and pos (at \)
            word = substrings[0].lower()
            posstring = substrings[1]
            pos = list(posstring)
            if word in wordinfodict:  # should be relatively fast
                #append pos list to pos field in wordinfo
                wordinfodict[word].pos = pos
        fobj.close()

        # if no pos from data, guess at parts of speech based on ending, 
        for word in wordinfodict:
            if wordinfodict[word].pos == []: #no POS
                if word.endswith("ing"):
                    wordinfodict[word].pos = "V"   # some may be i or t
                elif word.endswith("ed"):
                    wordinfodict[word].pos = "V"  # some may be nouns
                elif word.endswith("ly"):
                    wordinfodict[word].pos = "v"  # adverb (small v)   
                elif word.endswith("est"):
                    wordinfodict[word].pos = "A"  # adjective (actually superlative)
                elif word.endswith("tion"):
                    wordinfodict[word].pos = "V"  # big V  - some should be i or t
                elif word.endswith("es"):
                    wordwithoutes = word[:-2]
                    if wordwithoutes in wordinfodict:
                        if wordinfodict[wordwithoutes].pos:
                            wordinfodict[word].pos = wordinfodict[wordwithoutes].pos
                        else: # noending word found but no pos
                            wordinfodict[word].pos = "V"    # some of these definitely nouns, but can't tell
                    else:
                        wordinfodict[word].pos = "V"
                elif word.endswith("s"):
                    wordwithouts = word[:-1]
                    if wordwithouts in wordinfodict:
                        if wordinfodict[wordwithouts].pos:
                            wordinfodict[word].pos = wordinfodict[wordwithouts].pos
                        else: # noending word found but no pos
                            wordinfodict[word].pos = "V"    # some of these definitely nouns, but can't tell
                    else:
                        wordinfodict[word].pos = "V"

                else:
                    wordinfodict[word].pos = "N"
                
        print "pickling big info dict"
        #pickle it for later use
        # doing this one attribute at a time, because when I tried all it once it didn't unpickle properly

        try:
            pickleit(wordinfodict, "bigwordinfodict")
        except IOError, e:
            print "*** can't write big word data file:", e
      
