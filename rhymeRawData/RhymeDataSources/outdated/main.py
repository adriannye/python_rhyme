




"""
readTextFile.py -- read and parse text file
"""
import sys
import re
#from google.appengine.ext import db
MASCULINE = 1  #stress on last syllable
FEMININE = 0    # stress on second to last syllable
stresstranslate = {0:"Masculine", 1:"Feminine"}

class WordInfo: # represent a word and all associated data
    def __init__(self, spelling="", phonemes=[], rhymephonemes="", primstress=[], secstress=[], pos=[]):
        self.spelling, self.phonemes, self.rhymephonemes, self.primstress, self.secstress, self.pos = \
                       spelling, phonemes, rhymephonemes, primstress, secstress, pos
    def printall(self):
        print "Word: %s," % (self.spelling)
        for x in range(len(self.phonemes)):
            print "P%d is %s," % (x, self.phonemes[x])
        print "RP is %s," % (self.rhymephonemes)
        for x in range(len(self.primstress)):
            print "PS%d is %d," % (x, self.primstress[x])
        for x in range(len(self.secstress)):
            print "SS%d is %d," % (x, self.secstress[x])   
        for x in range(len(self.pos)):
            print "POS%d is %s," % (x, self.pos[x])
        print "" # newline


#class Rhymes            

# get filename
#fname = raw_input('Enter filename: ')
#print
if __name__ == '__main__':

    # attempt to open file for reading
    try:
        fobj = open("C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\Mobytestfile.txt", 'r')
    except IOError, e:
        print "*** can't open pronunciation data file:", e
    else:
        # process lines in file
        pos = []  #not filled in until reading POS file
        wordinfolist = []  # will be list of wordinfo class instances
        wordlist = [] #list of words only, used for dictionary creation
        linecount = 0
        print "running"
        for eachLine in fobj: # parse eachLine,
            # create data item for each field in WordInfo,
            # then create new WordInfo from it,
            # then add to WordList
          if eachLine == "\n":
                pass
          else:
            linecount=linecount+1
            print linecount
            substrings = eachLine.split(" ") # split into word and pronunciation (at space)
            spelling = substrings[0] # copy word to spelling field
            wordlist.append(spelling)
            #print spelling
            phonemes = substrings[1].split("/")  # split pronunciation into 1 field per phoneme
            primstress = [] # empty list we can append to in loop
            secstress = []
            #print "sp is %s," % spelling
            
            phonemes[-1] = phonemes[-1].replace("\n", "") # last phoneme has return on end. delete

            phonemescopy = phonemes[:] # copy list so we can edit original in for loop
            count = 0
            for x in range(len(phonemes)):  # len of original and copy same here, maybe not during
                if phonemescopy[x] == "": # delete blank phonemes - because of initial / and double //
                    del phonemes[x - count] # second time here original has shifted left
                    count=count+1  # amount original is shifted left

            if count: phonemescopy = phonemes[:] # do again if original changed
            count = 0
            for x in range(len(phonemes)):  # len of original and copy same here, maybe not during
                if phonemescopy[x] == ("'"):
                    primstress.append(x-count)  # stress phoneme becomes this when this item deleted 
                    del phonemes[x - count]  # modify original
                    count = count + 1
                elif "'" in phonemescopy[x]:
                    phonemes[x-count] = phonemes[x-count].replace("'", "")   # replace returns copy
                    primstress.append(x+1-count)   # append doesn't return copy, changes in place

                if phonemescopy[x] == (","):
                    secstress.append(x-count)  # stress phoneme becomes this when this item deleted 
                    del phonemes[x - count]  # modify original
                    count = count + 1
                elif "," in phonemescopy[x]:
                    phonemes[x-count] = phonemes[x-count].replace(",", "")   # replace returns copy
                    secstress.append(x+1 - count)   # append doesn't return copy, changes in place


            # rhyme phonemes go from last primary stressed syllable to end of word
            # but short words don't have marked stress
            # and some other words do not have marked stress

            if len(primstress) != 0:
                rhymephonemes = "".join(phonemes[primstress[-1]:])  # concatenate the last 6 phonemes, ignore empties
            else: #short word or no stress marked
                rhymephonemes = "".join(phonemes[-6:])  # concatenate the last 6 phonemes, ignore empties
                            
            #re.match('/(.*)/(.*)/(.*)', substrings[1])
   
            wordinfo = WordInfo(spelling, phonemes, rhymephonemes, primstress, secstress, pos)
            #wordinfo.printall()
            wordinfolist.append(wordinfo)
        fobj.close()

        # wordinfolist is now a list of wordinfo class instances, one per word
        
        # generate rhyme list as dictionary: key is word, value is list of wordinfo
        # first interate through words list and generate list of unique rhyme phoneme sequences 
        uniqueSequences = []
        for wordinfo in wordinfolist: # go through every word info 
            if wordinfo.rhymephonemes not in uniqueSequences:
                uniqueSequences.append(wordinfo.rhymephonemes)

        # create empty dictionary, unique phoneme sequence as key, empty value
        p2rdict = {}
        for sequence in uniqueSequences: 
            p2rdict[sequence] = []  # every value is an empty list at this point

        rhymephonemelist = []
        # append each rhyme word to value for appropriate key 
        for wordinfo in wordinfolist: # now add all words in their appropriate rhyme list
            p2rdict[wordinfo.rhymephonemes].append(wordinfo.spelling)
            rhymephonemelist.append(wordinfo.rhymephonemes) # this is for next dict

        # phoneme sequence to rhyme list dict now done
        
        # now create another dict keyed by word, value is rhyme phoneme sequence
        # this will be searched first when user types word,

        w2pdict = dict(zip(wordlist, rhymephonemelist))
        
        # get filename
        
        word2rhyme = raw_input('Enter word to rhyme: ')

        print p2rdict[w2pdict[word2rhyme]]

        
