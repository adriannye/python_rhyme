#!/usr/bin/python

import gdbm
import sys
import string
import os

if (os.environ.has_key("RHYMEPATH")):
    RHYMEPATH = os.environ["RHYMEPATH"]
else:
    RHYMEPATH = "/usr/share/rhyme"

WordNotFound = "word not found"

VERSION = "0.3"

class Rhyme:
    def __init__(self, path = RHYMEPATH):
        self.words = gdbm.open("%s/words.db" % (path))
        self.rhymes = gdbm.open("%s/rhymes.db" % (path))
        self.multiple = gdbm.open("%s/multiple.db" % (path))

    def getKey(self, word):
        try:
            return string.split(self.words[string.upper(word)], " ")[0]
        except KeyError:
            raise WordNotFound, string.lower(word)

    def getSyllables(self, word):
        try:
            return int(string.split(self.words[string.upper(word)], " ")[1])
        except KeyError:
            raise WordNotFound, string.lower(word)

    def getPronunciations(self, word):
        try:
            return string.split(self.multiple[string.upper(word)], " ")
        except KeyError:
            return [string.upper(word)]

    #returns a dictionary of lists
    #the keys are an int of the number of syllables
    #and the values are an alphabetized list of rhymes
    def rhyme(self, word):

        #inverts a dictionary, turning key->value into value->[keys]
        def invert(dict):
            inverted = {}

            for key in dict.keys():
                if (inverted.has_key(dict[key])):
                    inverted[dict[key]].append(string.lower(key))
                else:
                    inverted[dict[key]] = [string.lower(key)]

            return inverted

        
        toreturn = {}

        for pronunciation in self.getPronunciations(word):
            for rhyme in string.split(self.rhymes[self.getKey(pronunciation)],
                                      " "):
                if (not toreturn.has_key(rhyme)):
                    toreturn[rhyme] = self.getSyllables(rhyme)

        return invert(toreturn)

    #returns a tuple containing the minimum and maximum syllables
    #for a given word.. ("whitening" returns (2,3), for example)
    def syllables(self, word):
        min = 0
        max = 0
        
        for pronunciation in self.getPronunciations(word):
            syllables = self.getSyllables(pronunciation)
            if (min == 0):
                min = syllables
                max = syllables
            else:
                if (syllables > max):
                    max = syllables
                if (syllables < min):
                    min = syllables

        return (min, max)

def printRhymes(rhymes, stream = sys.stdout, width=80):
    def printRow(words, stream, width):
        wordsprinted = 0
        charsprinted = 0

        wordsize = 0
        while ((wordsprinted < len(words)) and
               ((charsprinted + wordsize + 2) < width)):
            if (wordsprinted != 0):
                stream.write(", ")
                charsprinted = charsprinted + 2

            wordsize = len(words[wordsprinted])
            stream.write(words[wordsprinted])
            wordsprinted = wordsprinted + 1
            charsprinted = charsprinted + wordsize


        return words[wordsprinted:]

    keys = rhymes.keys()
    keys.sort()

    for key in keys:
        r = rhymes[key]
        r.sort()
        prefix = "%s: " % (key)
        space = " " * (len(prefix))

        stream.write(prefix)
        r = printRow(r, stream, width - len(prefix))
        stream.write("\n")
        while (len(r) > 0):
            stream.write(space)
            r = printRow(r, stream, width - len(prefix))
            stream.write("\n")
        stream.write("\n")

def printHelp(stream):
    stream.write("Usage : rhyme [OPTIONS] word\n\n")
    stream.write("Search types:   (perfect rhyme is default)\n")
    stream.write("  -s, --syllable\treturns only the number of syllables\n\n")
    stream.write("Miscellaneous options:\n")
    stream.write("  -h, --help\t\tthis help message\n")
    stream.write("  -v, --version\t\tthis program's version\n\n")
    stream.write("Environment variables:\n\n")
    stream.write("RHYMEPATH\t\tthe directory of the database files\n\n")
    stream.write("The output is ordered by syllable count and alphabetized\n")

if (__name__ == '__main__'):
    import getopt

    r = Rhyme()

    syllablesearch = 0

    (options, args) = getopt.getopt(sys.argv[1:], "hsv",
                                    ["syllable","help","version"])

    for option in options:
        if ((option[0] == '-v') or (option[0] == '--version')):
            print("Rhyming Dictionary %s" % (VERSION))
            sys.exit(0)
        if ((option[0] == '-h') or (option[0] == '--help')):
            printHelp(sys.stdout)
            sys.exit(0)
        if ((option[0] == '-s') or (option[0] == '--syllable')):
            syllablesearch = 1

    try:
        if (not syllablesearch):
            printRhymes(r.rhyme(args[0]))
        else:
            syllables = r.syllables(args[0])
            if (syllables[0] != syllables[1]):
                print("%s-%s syllables" % (syllables[0], syllables[1]))
            else:
                if (syllables[0] == 1):
                    print("%s syllable" % (syllables[0]))
                else:
                    print("%s syllables" % (syllables[0]))
    except WordNotFound, w:
        print("*** Word \"%s\" wasn't found" % (w))
    except IndexError:
        printHelp(sys.stdout)
        
