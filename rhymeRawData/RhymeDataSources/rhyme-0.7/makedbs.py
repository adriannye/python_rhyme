#!/usr/bin/python

import string
#import gdbm
import re
import sys

#We convert this list of phenomes into single characters that we
#can join as a single string.  It makes life so much easier...
CONSONANTS = ['B','CH','D','DH',
            'F','G','HH','JH','K','L','M','N',
            'NG','P','R','S','SH','T','TH',
            'V','W','Y','Z','ZH']

CONSONANTLEN = len(CONSONANTS)
PHENOMES = CONSONANTS[:]

VOWELS = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY',
          'OW','OY','UH','UW']

STRESSES = ['0','1','2']

PRIMARYSTRESSES = []

#then we seed the data..DON'T PUT THIS IN A __MAIN__ CLAUSE!
index = len(PHENOMES)
for vowel in VOWELS:
    for stress in STRESSES:
        PHENOMES.append(vowel + stress)
        if (stress == '1'):
            PRIMARYSTRESSES.append(index)
        index = index + 1

#A helper routine.  Returns true if the item is in the list.
def contains(list, item):
    try:
        list.index(item)
        return 1
    except ValueError:
        return 0

NoStress = "no stress found"

def primaryStressIndex(phenomes):
    i = 0
    for phenome in phenomes:
        if (contains(PRIMARYSTRESSES, phenome)):
            return i
        else:
            i = i + 1
    raise NoStress

MULTIPLEPRONUNCIATION = re.compile(".+\(.+\)")

def isMultiplePronunciation(word):
    if (MULTIPLEPRONUNCIATION.match(word) == None):
        return 0
    else:
        return 1

def getWordPrefix(word):
    return word[0:string.index(word, "(")]

def keyAlreadyPresent(rhymekey, words, multiplelist):
    for m in multiplelist:
        if (rhymekey == words[m][0]):
            return 1
    else:
        return 0

def compileSourceDotC(maxline):
    return """#include <stdio.h>
#include <gdbm.h>
#include <stdlib.h>

/*This value is precalculated from the makedbs.py file.
  If the raw dictionary files are changed, this source file will be
  re-generated automatically.*/
#define MAX_LINE """ + `maxline + 1` + """

int main(int argc, char *argv[]) {
  FILE *input;
  GDBM_FILE output;

  int lines = 0;
  int i,j;
  char inputline[MAX_LINE];

  char key[MAX_LINE];
  char value[MAX_LINE];
  int keysize;
  int valuesize;

  datum keyd;
  datum valued;

  keyd.dptr = key;
  valued.dptr = value;

  if (argc != 3) {
    fprintf(stderr, 
	    \"*** Usage: compile <text input file> <gdbm output file>\\n\");
    exit(1);
  }

  input = fopen(argv[1], \"r\");

  if (input == NULL) {
    fprintf(stderr,
	    \"error opening %s\\n\", argv[1]);
    exit(1);
  }

  output = gdbm_open(argv[2], 0, GDBM_NEWDB, 0644, 0);

  while (fgets(inputline, MAX_LINE, input) != NULL) {
    keysize = 0;
    valuesize = 0;

    for (i = 0 ; inputline[i] != ' ' ; i++) {
      key[i] = inputline[i];
      keysize++;
    }
    i++;
    key[i] = '\\0';

    for (j=0; (inputline[i] != '\\n') && (inputline[i] != '\\0'); i++,j++) {
      value[j] = inputline[i];
      valuesize++;
    }

    value[j] = '\\0';

    keyd.dsize = keysize;
    valued.dsize = valuesize;

    if (gdbm_store(output, keyd, valued, GDBM_INSERT) == 1) {
      fprintf(stderr, \"Key %s is already present in database\\n\", key);
      exit(1);
    }

    lines++;
  }

  gdbm_sync(output);

  fclose(input);
  gdbm_close(output);

  printf(\"Inserted %d lines into %s\\n\", lines, argv[2]);

  return 0;
}
"""

if (__name__ == '__main__'):

    master = sys.stdin
    #master = open("cmudict.0.6-1")

    #worddb = gdbm.open("words.db","nf")
    #syllabledb = gdbm.open("syllables.db","nf")
    #rhymedb = gdbm.open("rhymes.db","nf")
    #multipledb = gdbm.open("multiple.db","nf")

    worddb = open(sys.argv[1],"w")
    #syllabledb = open("syllables.txt","w")
    rhymedb = open(sys.argv[2],"w")
    multipledb = open(sys.argv[3],"w")

    compile = open(sys.argv[4],"w")
    maxline = 0

    words = {}
    rhymes = {}
    multiples = {}

    try:
        line = master.readline()
        
        while (line):
            line = string.strip(line)

            if (line and (line[0] != "#")):
                syllables = 0

                split = re.split('\s+', string.strip(line))
                word = split[0]
                phenomes = []
                for phenome in split[1:]:
                    try:
                        index = PHENOMES.index(phenome)
                    except ValueError:
                        print("Unknown phoneme : %s" % (phenome))
                        sys.exit(1)
                        
                    if (index >= CONSONANTLEN):
                        syllables = syllables + 1
                    phenomes.append(index)
                phenomes.reverse()

                try:
                    stress = primaryStressIndex(phenomes)
                except NoStress:
                    print("No stress for %s" % word)
                    line = master.readline()
                    continue

                #This is the key
                s = string.join(map(lambda x: chr(x + 33),
                                phenomes[0:primaryStressIndex(phenomes) + 1]),
                                "")

                if (isMultiplePronunciation(word)):
                    prefix = getWordPrefix(word)
                    if (multiples.has_key(prefix)):
                        #Check all previously-added spellings for
                        #identical keys.  If any identical pronunciations
                        #have the same key, leave the word out.
                        if (keyAlreadyPresent(s, words, multiples[prefix])):
                            print("Multiple identical rhyme for %s" % \
                                  (word))
                            line = master.readline()
                            continue
                        else:
                            multiples[prefix].append(word)
                    else:
                        try:
                            key = words[prefix][0]
                        except KeyError:
                            key = None
                            
                        if (s == key):
                            print("Multiple identical rhyme for %s" % \
                                  (word))
                            line = master.readline()
                            continue
                        else:
                            multiples[prefix] = [prefix, word]
                
                #print("%s - %s - %s" % (word, phenomes,
                #                        primaryStressIndex(phenomes)))

                #syllabledb[word] = `syllables`
                #worddb[word] = s

                #syllabledb.write("%s %s\n" % (word, syllables))
                words[word] = (s, syllables)
                #worddb.write("%s %s %s\n" % (word, s, syllables))

                if (rhymes.has_key(s)):
                    rhymes[s].append(word)
                else:
                    rhymes[s] = [word]
                
            line = master.readline()

        wordkeys = words.keys()
        wordkeys.sort()

        for key in wordkeys:
            worddb.write("%s %s %s\n" % (key, words[key][0], words[key][1]))

        for key in rhymes.keys():
            rhymes[key].sort()
            #rhymedb[key] = string.join(rhymes[key], " ")
            rhymestring = "%s %s\n" % (key, string.join(rhymes[key], " "))
            if (len(rhymestring) > maxline):
                maxline = len(rhymestring)
            rhymedb.write(rhymestring)

        for key in multiples.keys():
            multiples[key].sort()
            multiples[key].reverse()
            #multipledb[key] = string.join(multiples[key], " ")
            multipledb.write("%s %s\n" % (key, string.join(multiples[key])))
        #print(rhymes)

        compile.write(compileSourceDotC(maxline))
        
    finally:
        #syllabledb.close()
        worddb.close()
        rhymedb.close()
        multipledb.close()

        compile.close()
        
        master.close()
