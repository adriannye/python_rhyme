parsepron.py #  read and parse pronunciation and part of speech files, generate dicts for word info and rhyme list
	mypronsrc - input pronunciation file - edited from CMU 7
	Mobypossrc - Moby word part of speech file
	bigwordinfodict - key is word, value is class WordInfo 


prunewords.py # read exhaustive word info dict and common word file,
		and generate smaller word info dict from the words in common 
		also generate cut word list for use in addendings.py
	bigwordinfodict - input
	english-words10+20 - input
	prunedwordinfodict - smaller version of bigwordinfodict, only words
				that were found in english-words as well
	cutwordfile = words in english-words not found in bigwordinfodict
	
genrhymes # opens pruned word dict, generate dict where key is phoneme sequence, value is list of words
	p2rdict - key is rhyme phoneme, value is list of words

userrhyme  # take user input of word, print list of rhymes

OUTDATED:
from Moby Pron version:
addendings.py - read big word info file and cut word file,
add trial endings to each word in big list and see if result is in cut words, 
then generate new pron file from the words in common. 
	bigwordinfodict - input
	cutwordfile - input
	wordgenpron - output