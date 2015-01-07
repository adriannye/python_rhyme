#include "getopt.h"
#include <gdbm.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*useful setup info for the Rhyming Dictionary
  Copyright (C) 2000 Brian Langenberger
  Released under the terms of the GNU Public License.
  See the file "COPYING" for full details.*/

#ifndef DEFAULT_RHYMEPATH
#define DEFAULT_RHYMEPATH "/usr/share/rhyme"
#endif

#define WORDS_NAME "/words.db"
#define RHYMES_NAME "/rhymes.db"
#define MULTIPLES_NAME "/multiple.db"

#define RHYME_ENV "RHYMEPATH"

#define VERSION "0.7"

/*I only have three flags so the binary representation is rather simple*/
#define FLAG_SYLLABLE 1
#define FLAG_INTERACTIVE 2
#define FLAG_MERGED 4

/*something to print if gdbm dies horribly*/
void fatalError(char s[]);

void rhymeSetup(GDBM_FILE *wordfile, GDBM_FILE *rhymefile, 
		GDBM_FILE *multiplefile,
		int *flags, int argc, char *argv[], int *wordindex);

GDBM_FILE openGDBMFile(char *dir, char *file);

void printHelp(FILE *stream);

