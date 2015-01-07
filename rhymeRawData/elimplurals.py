
import sys
import pickle
workingdir = "C:\\Documents and Settings\\Adrian Nye\\My Documents\\FamilyRhyme\\rhymeRawData\\"

if __name__ == '__main__':
    print "starting"
    #def main():
    # attempt to open file for reading
    try:
        fobj = open((workingdir + "english-words35edited.txt"), 'r')
    except IOError, e:
        print "*** can't open in data file:", e
    else:
        # process lines in file
        worddict = {} 
        wordlist = []  
        for word in fobj: # parse eachLine,
            # create data item for each field in WordInfo,
            # then create new WordInfo from it,
            # then add to WordList
            word = word.strip()
            worddict[word] = word 
            wordlist.append(word)

        fobj.close()

        for word in wordlist:
            if word[-1] == 's':

                without = word[:-1]
                if without in worddict:
                    wordlist.remove(word)

        try:
            fobj = open((workingdir + "english-words35out.txt"), 'w')
        except IOError, e:
            print "*** can't open out file:", e
        else:
            for word in wordlist:
                
                fobj.write(word)
                fobj.write("\n")

            fobj.close()

