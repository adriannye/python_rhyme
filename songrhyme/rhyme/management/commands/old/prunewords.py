
"""
prunewords.py -- read exhaustive word info file and common word file,
and generate new word info file from the words in both.
"""
import sys
import marshal
from pickleit import *
from wordinfo import WordInfo

workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

if __name__ == '__main__':
    # attempt to open file for reading
    print "Stage 2: reading big word dict"
    try:
        wordinfo = unpickleit("bigwordinfodict")
    except IOError, e:
        print "*** can't open big word data file:", e
    else:
        print "reading common word list"
        try:
            wordlistfile = open((workingdir + "english-words10+20+35.txt"), 'r')
        except IOError, e:
            print "*** can't open word list file:", e
        else:
        # process lines in file
            #posmissing = []
            print "in here"
            cutwordlist = []
            newwordinfo = {} # this dict will contain only the words in common
            commonwordlist = []
            commoncount = 0

            for line in wordlistfile: # parse eachLine,

                if line == "\n":
                    continue   # ignore blank lines if any

                word = line.rstrip() # delete trailing whitespace and/or newline

                if word in wordinfo:
                    commonwordlist.append(word)
                    newwordinfo[word] = wordinfo[word].rhymephonemes
                    #newwordinfo[line].primstress = wordinfo[line].primstress
                    #newwordinfo[line].phonemes = wordinfo[line].phonemes
                    #newwordinfo[line].rhymephonemes = 
                    #newwordinfo[line].secstress = wordinfo[line].secstress
                    #newwordinfo[line].pos = wordinfo[line].pos
                    #print "new copy is %s" % newwordinfo[line].phonemes                    
                 
                    commoncount +=1

                    #if newwordinfo[line].pos == []:
                    #   posmissing.append(line)

                else:            
                    cutwordlist.append(word)

            wordlistfile.close()

            print "words in both: %d" % commoncount
            print "pickling pruned word info dict"
            
            #pickle it for later use
            pickleit(newwordinfo, "word2phonemeseqdict")
            pickleit(commonwordlist, "commonwordlist")
            #marshalit(newwordinfo, "word2phonemeseqdict")
            try:
                w2pdecfile = open((workingdir + "w2pdec.py"), 'w')
            except IOError, e:
                print "*** can't open out dec file:", e
            else:
                w2pdecfile.write('word2phonemeseqdict = {\n')
                for word in commonwordlist:
                    w2pdecfile.write('"%s":"%s",\n' % (word, newwordinfo[word]))
                w2pdecfile.write('}\n')
                w2pdecfile.close()
                
            print "saving cutwordlist"

            try:
                cutwordlistfile = open((workingdir + "cutwordlist"), 'w')
            except IOError, e:
                print "*** can't open cut word list file:", e
            else:
                for word in cutwordlist:
                    cutwordlistfile.write(word + "\n")
                cutwordlistfile.close()

            print "saving posmissingwordlist"
"""
            try:
                posmissinglistfile = open((workingdir + "posmissinglist"), 'w')
            except IOError, e:
                print "*** can't open pos missing list file:", e
            else:
                for word in posmissing:
                    posmissinglistfile.write(word + "\n")
                posmissinglistfile.close()
                """
