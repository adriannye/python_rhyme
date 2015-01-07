
"""
wordinfo.py -- define word info class and universal utility stuff
"""

class WordInfo: # list representing all associated data for a word
    pass
    def __init__(self, phonemes=[], rhymephonemes="", pos=[]):
        self.phonemes, self.rhymephonemes, self.pos = \
                       phonemes, rhymephonemes, pos
    def printall(self):
        for x in range(len(self.phonemes)):
            print "P%d is %s," % (x, self.phonemes[x])
        print "RP is %s," % (self.rhymephonemes)
        for x in range(len(self.pos)):
            print "POS%d is %s," % (x, self.pos[x])
        print "" # newline


