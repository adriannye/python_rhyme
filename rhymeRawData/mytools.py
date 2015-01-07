
"""
mytools.py --
functions used to generate and try rhymes
"""
import sys
from pickleit import *
#from google.appengine.ext import db
from wordinfo import WordInfo
from tables import *
import userrhyme 

def remove_cons(phonemeseq, index):
    stringlist=list(phonemeseq)
    del stringlist[index]
    newseq=''.join(stringlist)
    return newseq

def replace_cons(phonemeseq, index, char):
    stringlist=list(phonemeseq)
    stringlist[index] = char
    newseq=''.join(stringlist)
    return newseq

def add_cons(phonemeseq, char):
    newseq=phonemeseq + char
    return newseq


def find_consonants(phonemeseq):
    consecutive = -1 #  consecutive consonants if found becomes index
    consonant_indexes = [] # list of integer positions of consonants in rhyme phoneme sequence
    for i in range(len(phonemeseq)):  # scan sequence from left
        if phonemeseq[i] in cons_family:
            consonant_indexes.append(i)
    num_consonants = len(consonant_indexes)
    if num_consonants > 1: #at least 2 consonants
        for i in range(num_consonants-1):
            if consonant_indexes[i+1]-consonant_indexes[i] == 1:
                #consecutive consonants
                consecutive = consonant_indexes[i]
    return consecutive, consonant_indexes
    
def  try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list):
    # replace consonant at consonant_index with trial_cons and test if valid word
    # if valid word then return list of rhymes
    newseq = replace_cons(phonemeseq, consonant_index, trial_cons)
    if newseq in p2rdict:
        newrhymelist = p2rdict[newseq]
        string = "<b>" + trial_cons + ' ' + "sound:</b>"
	list.append(string)
	[list.append(rhyme) for rhyme in newrhymelist]
    else: #no rhyme found
        pass

def make_rhymes(p2rdict, phonemeseq, consonant_indexes, kind, list):
    # vowel sounds stay the same
    # categorize consonant after stressed vowel and replace with relatives,
    # then see if we generated a phoneme sequence that exists (matches real words)
    # if phoneme sequence exists, add those rhymes to list
    for consonant_index in consonant_indexes: # for each consonant
        make_rhyme(p2rdict, phonemeseq, consonant_index, kind, list)

   
def make_rhyme(p2rdict, phonemeseq, consonant_index, kind, list):
    char = phonemeseq[consonant_index] # current value of char to be modified
    # now build list of replacements according to family
    if cons_family[char] == "voiced_fricative":
        # try companions, then unvoiced
        for trial_cons in cons_family_list["voiced_fricative"]:
            if trial_cons == char: #skip self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
            
        for trial_cons in cons_family_list["unvoiced_fricative"]:
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
            
    elif cons_family[char] == "unvoiced_fricative":
        # try companions, then voiced
        for trial_cons in cons_family_list["unvoiced_fricative"]:
            if trial_cons == char: #skip self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
            
        for trial_cons in cons_family_list["voiced_fricative"]:
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

    elif cons_family[char] == "voiced_plosive":
        i = cons_family_list["voiced_plosive"].index(char)  # index of first char
        # first try item i in other plosive list
        partner = cons_family_list["unvoiced_plosive"][i] # used later to skip

        # try partner
        trial_cons = cons_family_list["unvoiced_plosive"][i]
        try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

        # try other unvoiced plosives
        for trial_cons in cons_family_list["voiced_plosive"]: 
            if trial_cons == char: #skip self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

        # try voiced plosives
        for trial_cons in cons_family_list["unvoiced_plosive"]:
            if trial_cons == partner: #tried earlier
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
        # try partner, then companions, then other 2
        # for g can be long a,e,o u or short u
    elif cons_family[char] == "unvoiced_plosive":
        # try partner, then companions, then other 2
        # for g can be long a,e,o u or short u

        # find partner
        i = cons_family_list["unvoiced_plosive"].index(char)  # index of first char
        # first try item i in other plosive list
        partner = cons_family_list["voiced_plosive"][i] # used later to skip

        # try partner
        trial_cons = cons_family_list["voiced_plosive"][i]
        try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

        # try other unvoiced plosives
        for trial_cons in cons_family_list["unvoiced_plosive"]: 
            if trial_cons == char: #skip self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

        # try voiced plosives
        for trial_cons in cons_family_list["voiced_plosive"]:
            if trial_cons == partner: #tried earlier
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
                        
    elif cons_family[char] == "nasal":
        for trial_cons in cons_family_list["nasal"]:
            if trial_cons == char: #self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)

    elif cons_family[char] == "unique":
        for trial_cons in cons_family_list["unique"]:
            if trial_cons == char: #self
                continue
            try_rhymes(p2rdict, phonemeseq, consonant_index, trial_cons, kind, list)
        # for L and R in pair, keep first and replace second.
        # if alone, try others in this group
    else:
        pass #shouldn't happen
    

