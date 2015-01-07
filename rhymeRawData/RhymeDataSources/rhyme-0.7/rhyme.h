#include <stdio.h>
#include <stdlib.h>
#include <gdbm.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <readline.h>
#include <history.h>
#include "setup.h"

/*The initial declarations for the Rhyming Dictionary
  Copyright (C) 2000 Brian Langenberger
  Released under the terms of the GNU Public License.
  See the file "COPYING" for full details.*/

/*The maximum letters a word has..this is 23 + null and is calculated
  from the actual data file.  Hopefully new additions to the english
  language will not become overly common.*/
#define MAX_WORDLENGTH 24

/*The maximum phenomes is 20..this assumes all are syllables + null
  (which is ridiculous, but better to err on the side of caution)*/
#define MAX_SYLLABLES 21

/*These are for pretty-printing output*/
#define STARTROWSTRING ": "
#define INDENTROWSTRING "   "
#define PADSTRING ", "

#define SWAPSYLLABLEKEY "."
#define SWAPMERGEDKEY ","
#define HELPKEY "?"

#define PROMPT_RHYME "RHYME> "
#define PROMPT_MERGED "RHYME-MERGED> "
#define PROMPT_SYLLABLE "SYLLABLE> "

/*This should be self-explanatory.
  The "next" variable is for stringing words together into a group.*/
struct RhymeWord {
  char word[MAX_WORDLENGTH];
  int syllables;
  struct RhymeWord *next;
};

void displayRhymes(char *word, int flags,
		   GDBM_FILE wordfile,
		   GDBM_FILE rhymefile,
		   GDBM_FILE multiplefile);

/*Returns the number of digits in an integer.
  103 has 3 digits, for example*/
int countdigits(int i);

void stripNewLine(char *s);

int screenWidth();

/*copies the string data from d to s, ensuring null termination*/
void datumToString(char *s, datum d, int maxlength);

/*these two functions pull the word or syllable data from the
  words.db gdbm datafile - I've multiplexed them to save 10 megs*/
void keyFromWord(char *s, datum d, int maxlength);
int syllablesFromWord(datum d, int maxlength);

/*Prints out the list of rhymes to the given width, first by
  sorting them (with sortWords()) and then by calling
  print_rhyme_row() on each.*/
void print_rhymes(struct RhymeWord *head, FILE *stream, int width);

/*takes two sorted RhymeWord lists and returns them sorted with
  duplicates removed and free()ed*/
struct RhymeWord *mergeWords(struct RhymeWord *left, struct RhymeWord *right);

/*Because we're sorting first by syllable count and then alphabetically,
  and because the number of syllables is small (< 20) we'll use a
  bucket sort on them.  In a stack-like fashion, this takes the
  reverse-sorted linked-list and re-stacks them into the array of
  RhymeWord pointers - which restores them to the proper order.*/
void sortWords(struct RhymeWord *head, struct RhymeWord *syllables[]);

/*Prints the given row (assumed to have all the same syllable count
  and pre-sorted for us) to the given width on the given stream.*/
void print_rhyme_row(struct RhymeWord *row, FILE *stream, int width);

/*Frees up our allocated memory.*/
void freeWords(struct RhymeWord *head);

/*quickly prints out the list of RhymeWords (for debugging)*/
void printWordList(struct RhymeWord *head);

/*returns the number of syllables in the word, or -1 if not found*/
int syllables(GDBM_FILE wordfile, char *word);

/*this swaps the query type for interactive mode*/
void swapSyllableModes(int *flags);

void swapMergedModes(int *flags);

/*checks for all rhymes in the list and returns them merged*/
struct RhymeWord *findAllRhymes(GDBM_FILE wordfile, GDBM_FILE rhymefile, 
		   struct RhymeWord *list);

/*finds and prints all the rhymes for the given word*/
struct RhymeWord *rhyme(GDBM_FILE wordfile, GDBM_FILE rhymefile, 
			char *word);

/*sets the range of syllable counts for the given list of words
  (in order to handle multiple pronunciations*/
void countSyllables(GDBM_FILE wordfile, struct RhymeWord *list,
		    int *min, int *max);

/*takes a string of words returned from gdbm and returns a linked-list
  of them in lowercase - suitable for display with syllable counts added*/
struct RhymeWord *parseWordList(GDBM_FILE wordfile, char *list, 
				int length);

/*takes a string of pronunciations and returns a linked-list of them
  still in uppercase - unsuitable for display with no syllable counts*/
struct RhymeWord *parsePronounceList(char *list, int length);

void printFindingRhyme(char *word);

void printNotFound(FILE *stream, char *word);

void printInteractiveHelp(FILE *stream);
