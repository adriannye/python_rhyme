#include "rhyme.h"

/*The main code for the Rhyming Dictionary
  Copyright (C) 2000 Brian Langenberger
  Released under the terms of the GNU Public License.
  See the file "COPYING" for full details.*/

int main(int argc, char *argv[]) {
  /*first the pointers to our data files*/
  GDBM_FILE wordfile;
  GDBM_FILE rhymefile;
  GDBM_FILE multiplefile;

  /*helper variables to convert from lower to upper case*/
  char *word;

  int wordindex;

  /*flags from the setup file*/
  int flags = 0;

  rhymeSetup(&wordfile, &rhymefile, &multiplefile, &flags,
	     argc, argv, &wordindex);

  using_history();

  rl_bind_key('\t', rl_insert);

  if (flags & FLAG_INTERACTIVE) {
    printf("Rhyming Dictionary %s - interactive mode\n", VERSION);

    printInteractiveHelp(stdout);

    if (flags & FLAG_SYLLABLE) {
      word = readline(PROMPT_SYLLABLE);
    } else if (flags & FLAG_MERGED) {
      word = readline(PROMPT_MERGED);
    } else {
      word = readline(PROMPT_RHYME);
    }

    /*word = readline((flags & FLAG_SYLLABLE) ? PROMPT_SYLLABLE : 
      (flags & FLAG_MERGED) ? PROMPT_MERGED : PROMPT_RHYME);*/

    while ((word != NULL) && (strlen(word) > 0)) {
      if (strcmp(SWAPSYLLABLEKEY, word) == 0) {
	swapSyllableModes(&flags);
      } else if (strcmp(SWAPMERGEDKEY, word) == 0) {
	swapMergedModes(&flags);
      } else if (strcmp(HELPKEY, word) == 0) {
	printInteractiveHelp(stdout);
      } else {
	displayRhymes(word, flags, wordfile, rhymefile, multiplefile);
	add_history(word);
      }

      free(word);

      /*word = readline((flags & FLAG_SYLLABLE) ? PROMPT_SYLLABLE : 
	PROMPT_RHYME);*/

      if (flags & FLAG_SYLLABLE) {
	word = readline(PROMPT_SYLLABLE);
      } else if (flags & FLAG_MERGED) {
	word = readline(PROMPT_MERGED);
      } else {
	word = readline(PROMPT_RHYME);
      }

    }
  } else {
    word = argv[wordindex];

    displayRhymes(word, flags, wordfile, rhymefile, multiplefile);
  }

  clear_history();

  gdbm_close(wordfile);
  gdbm_close(rhymefile);
  gdbm_close(multiplefile);
  
  return 0;
}

void displayRhymes(char *word, int flags,
		   GDBM_FILE wordfile,
		   GDBM_FILE rhymefile,
		   GDBM_FILE multiplefile) {
  int i;

  char capword[MAX_WORDLENGTH];

  /*variables for finding syllable ranges*/
  int low = 0;
  int high = 0;

  /*pronunciations stores the list of pronunciations for the given word*/
  struct RhymeWord *pronunciations;
  
  /*Pointers for traversing the list of pronuncations in the event of a
    non-merged search*/
  struct RhymeWord *thisword;
  struct RhymeWord *nextword;

  /*and rhymes is the actual result*/
  struct RhymeWord *rhymes;

  /*along with a couple of helper variables to use with the multiple-file*/
  datum pronounceword;
  datum pronouncelist;


  for (i = 0 ; word[i] != '\0'; i++) {
    capword[i] = toupper(word[i]);
  }
  capword[i] = '\0';

  /*generate a list of pronunciations for the given word*/
  pronounceword.dptr = capword;
  pronounceword.dsize = strlen(capword);
  pronouncelist = gdbm_fetch(multiplefile, pronounceword);

  /*whether a word has multiple pronunciations or not,
    put the result into the pronunciations list*/
  if (pronouncelist.dptr != NULL) {
    pronunciations = parsePronounceList(pronouncelist.dptr,
					pronouncelist.dsize);
  } else {
    pronunciations = (struct RhymeWord *)malloc(sizeof(struct RhymeWord));
    strncpy(pronunciations->word, capword, MAX_WORDLENGTH);
    pronunciations->syllables = 0;
    pronunciations->next = NULL;
  }

  if (flags & FLAG_SYLLABLE) {
    /*do the actual syllable counting*/
    countSyllables(wordfile, pronunciations, &low, &high);

    /*and print the result*/
    if (low == -1) {
      printNotFound(stderr, word);
    } else if (low == high) {
      printf("%d %s", high, (high == 1) ? "syllable\n" : "syllables\n");
    } else {
      printf("%d-%d syllables\n", low, high);
    }
  } else if (flags & FLAG_MERGED) {
    printFindingRhyme(word);

    /*get the list of perfect rhymes*/
    rhymes = findAllRhymes(wordfile, rhymefile, pronunciations);

    /*and print them (if any)*/
    if (rhymes != NULL) {
      print_rhymes(rhymes, stdout, screenWidth());
      freeWords(rhymes);
    } else {
      printNotFound(stderr, word);
    }
  } else {
    /*If there is only a single pronunciation, we must handle errors
      differently than if there are several, hence the if-then clause*/
    if (pronunciations->next == NULL) {
      printFindingRhyme(pronunciations->word);
      rhymes = rhyme(wordfile, rhymefile, pronunciations->word);
      if (rhymes == NULL) {
	printNotFound(stderr, pronunciations->word);
      } else {
	print_rhymes(rhymes, stdout, screenWidth());
	freeWords(rhymes);
      }
    } else {
      thisword = pronunciations;

      while (thisword != NULL) {
	nextword = thisword->next;

	rhymes = rhyme(wordfile, rhymefile, thisword->word);

	if (rhymes == NULL) {
	  /*If a pronuncation in the multiple pronunciation list
	    isn't among the rhymes list, the data is screwed up.
	    So, the best solution is to simply ignore the non-result
	    rather than print an error about it
	    printNotFound(stderr, thisword->word);*/
	} else {
	  printFindingRhyme(thisword->word);

	  print_rhymes(rhymes, stdout, screenWidth());
	  freeWords(rhymes);
	}

	thisword = nextword;
      }
    }
  }

  /*free up space prior to exit  (it's just good practice) */

  freeWords(pronunciations);  /*first the parsed linked-list result*/
  free(pronouncelist.dptr);   /*the result from multiple.db*/
}

void datumToString(char *s, datum d, int maxlength) {
  int length;
  int i;

  /*the max length of datum's size or the maxlength of the s string*/
  if (d.dsize < maxlength)
    length = d.dsize;
  else
    length = maxlength;

  for (i = 0 ; i < length ; i++)
    s[i] = d.dptr[i];

  s[i] = '\0';
}

void keyFromWord(char *s, datum d, int maxlength) {
  int i;
  for (i = 0 ; (d.dptr[i] != ' ') && (i < maxlength) ; i++) {
    s[i] = d.dptr[i];
  }

  s[i] = '\0';
}

int syllablesFromWord(datum d, int maxlength) {
  int i,j;
  char syllables[5];

  for (i = 0 ; d.dptr[i] != ' ' ; i++)
    /*do nothing*/;

  for (j = 0,i++ ; (j < maxlength) && (i < d.dsize) ; i++,j++) {
    syllables[j] = d.dptr[i];
  }

  syllables[j] = '\0';

  return atoi(syllables);
}

int syllables(GDBM_FILE wordfile, char *word) {
  datum w;
  datum result;
  int toreturn;
  /*char syllablestring[5];*/

  w.dptr = word;
  w.dsize = strlen(word);

  result = gdbm_fetch(wordfile, w);

  if (result.dptr == NULL) {
    return -1;
  } else {
    /*datumToString(syllablestring, result, 5);
    toreturn = atoi(syllablestring);*/
    toreturn = syllablesFromWord(result, 5);

    free(result.dptr);
    return toreturn;
  }
}


struct RhymeWord *findAllRhymes(GDBM_FILE wordfile, GDBM_FILE rhymefile, 
		   struct RhymeWord *list) {
  struct RhymeWord *head;

  if (list == NULL) {
    return NULL;
  } else {
    head = rhyme(wordfile, rhymefile, list->word);
    return mergeWords(head, findAllRhymes(wordfile, rhymefile, list->next));
  }
}

struct RhymeWord *rhyme(GDBM_FILE wordfile, GDBM_FILE rhymefile, char *word) {
  datum search;
  datum rhymekey;

  char searchstring[MAX_WORDLENGTH];
  datum searchkey;
  datum words;

  struct RhymeWord *results;

  search.dptr = word;
  search.dsize = strlen(word);

  rhymekey = gdbm_fetch(wordfile, search);

  if (rhymekey.dptr == NULL) {
    return NULL;
  }

  keyFromWord(searchstring, rhymekey, MAX_WORDLENGTH);
  searchkey.dptr = searchstring;
  searchkey.dsize = strlen(searchstring);

  words = gdbm_fetch(rhymefile, searchkey);

  /*printf("%s\n\n", words.dptr);*/

  results = parseWordList(wordfile, words.dptr, words.dsize);

  /*print_rhymes(results, stdout, 80);

  freeWords(results);*/

  free(words.dptr);
  free(rhymekey.dptr);

  return results;
}

void countSyllables(GDBM_FILE wordfile, struct RhymeWord *list,
		    int *min, int *max) {
  int s;

  if (list == NULL) {
    return;
  } else {
    s = syllables(wordfile, list->word);
    if (*min == 0) { /*we're on the first search*/
      *min = s;
      *max = s;
    } else {
      if (s < *min) *min = s;
      if (s > *max) *max = s;
    }

    countSyllables(wordfile, list->next, min, max);
  }
}

struct RhymeWord *parseWordList(GDBM_FILE syllablefile, char *list, 
				int length) {
  int i,j,k;
  int wordstart = 0;
  char subword[MAX_WORDLENGTH];

  struct RhymeWord *toreturn = NULL;
  struct RhymeWord *word;

  for (i = 0 ; i <= length ; i++) {
    /*find the next space or end of the result list*/
    if (isspace((int)list[i]) || (i == length)) {
      for (j = wordstart,k = 0; j < i ; j++, k++) {
	subword[k] = list[j];
      } 
      subword[k] = '\0';
      wordstart = j + 1;

      /*printf("->%s<-\n", subword);*/

      word = (struct RhymeWord *)malloc(sizeof(struct RhymeWord));

      /*this is a combination strncpy/tolower to put the sub-word into
       the RhymeWord structure created above*/
      for (j = 0 ; (subword[j] != '\0') && (j < MAX_WORDLENGTH) ; j++) {
	word->word[j] = tolower(subword[j]);
      }
      word->word[j] = '\0';
      word->syllables = syllables(syllablefile, subword);
      word->next = toreturn;
      toreturn = word;
    }
  }

  return toreturn;
}

struct RhymeWord *parsePronounceList(char *list, int length) {
  /*nearly a carbon copy of parseWordList(),
    but with a significantly different purpose*/

  int i,j,k;
  int wordstart = 0;
  char subword[MAX_WORDLENGTH];

  struct RhymeWord *toreturn = NULL;
  struct RhymeWord *word;

  for (i = 0 ; i <= length ; i++) {
    if (isspace((int)list[i]) || (i == length)) {
      for (j = wordstart,k = 0; j < i ; j++, k++) {
	subword[k] = list[j];
      } 
      subword[k] = '\0';
      wordstart = j + 1;

      /*printf("->%s<-\n", subword);*/

      word = (struct RhymeWord *)malloc(sizeof(struct RhymeWord));

      strncpy(word->word, subword, MAX_WORDLENGTH);
      word->word[j] = '\0';
      word->syllables = 0;
      word->next = toreturn;
      toreturn = word;
    }
  }

  return toreturn;
}

int screenWidth() {
  struct winsize size;

  if (isatty(1) == 0)
    return 80;
  else {
    if (ioctl(1, TIOCGWINSZ, (char *)&size) < 0)
      return 80;
    else
      return (size.ws_col > MAX_WORDLENGTH) ? size.ws_col : MAX_WORDLENGTH;
  }
}

int countdigits(int i) {
  /*one of my favortite recursive routines*/
  if (i <= 9) {
    return 1;
  } else {
    return 1 + countdigits(i / 10);
  }
}

void stripNewLine(char *s) {
  int i;

  for (i = 0 ; s[i] != '\0' ; i++) {
    if (s[i] == '\n') {
      s[i] = '\0';
      return;
    }
  }
}

void print_rhymes(struct RhymeWord *head, FILE *stream, int width) {
  struct RhymeWord *syllables[MAX_SYLLABLES];
  int i;

  /*printWordList(head);*/

  for (i = 0 ; i < MAX_SYLLABLES ; i++)
    syllables[i] = NULL;
  
  sortWords(head, syllables);

  for (i = 0 ; i < MAX_SYLLABLES ; i++) {
    if (syllables[i] != NULL);
      print_rhyme_row(syllables[i], stream, width);
  }
}

void print_rhyme_row(struct RhymeWord *head, FILE *stream, int width) {
  struct RhymeWord *current;
  struct RhymeWord *next;
  int sent = 0;
  int wordwidth;
  int firstword = 1;

  int startrowwidth = strlen(STARTROWSTRING);
  int indentrowwidth = strlen(INDENTROWSTRING);
  int padwidth = strlen(PADSTRING);

  if (head == NULL)
    return;

  current = head;

  fprintf(stream, "%d%s", current->syllables, STARTROWSTRING);
  sent += (countdigits(current->syllables), startrowwidth);

  while (current != NULL) {
    next = current->next;
    wordwidth = strlen(current->word);
    if ((sent + wordwidth + padwidth) <= width) {
      if (!firstword) {
	fprintf(stream, "%s%s", PADSTRING, current->word);
	sent += (wordwidth + padwidth);
      } else {
	firstword = 0;
	fprintf(stream, "%s", current->word);
	sent += (wordwidth + indentrowwidth);
      }
    } else {
      firstword = 0;
      fprintf(stream, "\n%s%s", INDENTROWSTRING, current->word);
      sent = (indentrowwidth + wordwidth);
    }
    /*printf("%s - %d\n", current->word, current->syllables);*/
    current = next;
  }

  fprintf(stream, "\n\n");
}

void freeWords(struct RhymeWord *head) {
  struct RhymeWord *current;
  struct RhymeWord *next;

  current = head;

  while (current != NULL) {
    next = current->next;
    free(current);
    current = next;
  }
}

void printWordList(struct RhymeWord *head) {
  if (head != NULL) {
    printf("%s - %d\n", head->word, head->syllables);
    printWordList(head->next);
  } else
    return;
}

void sortWords(struct RhymeWord *head, struct RhymeWord *syllables[]) {
  struct RhymeWord *current;
  struct RhymeWord *next;

  current = head;

  while (current != NULL) {
    next = current->next;
    current->next = syllables[current->syllables];
    syllables[current->syllables] = current;
    current = next;
  }
}

struct RhymeWord *mergeWords(struct RhymeWord *left, struct RhymeWord *right) {
  /*This worked the first time I wrote it ... so I don't trust it
    It's a zipper-esque merge routine for merging the left and right lists
    and returning one sorted list.  Redundant items are free()ed*/

  int compare;
  struct RhymeWord *next;

  if (left == NULL) {
    return right;
  } else if (right == NULL) {
    return left;
  } else {
    /*if it's not a trivial case of one list being empty...*/

    compare = strcmp(left->word, right->word);

    if (compare == 0) {   /*if both are equal, free up right and continue*/
      next = right->next;
      free(right);
      left->next = mergeWords(left->next, next);
      return left;
    } else if (compare > 0) { /*left is higher asciibetically than right*/
      left->next = mergeWords(left->next, right);
      return left;
    } else {                  /*right is higher*/
      right->next = mergeWords(left, right->next);
      return right;
    }
  }
}

void swapSyllableModes(int *flags) {
  if (*flags & FLAG_SYLLABLE) {
    *flags &= ~FLAG_SYLLABLE;
  } else {
    *flags |= FLAG_SYLLABLE;
  }
}

void swapMergedModes(int *flags) {
  if (*flags & FLAG_MERGED) {
    *flags &= ~FLAG_MERGED;
  } else {
    *flags |= FLAG_MERGED;
  }
}

void printFindingRhyme(char *word) {
  int i;

  printf("Finding perfect rhymes for ");
  for (i = 0 ; word[i] != '\0'; i++) {
      putchar(tolower(word[i]));
    }
  printf("...\n");
}

void printNotFound(FILE *stream, char *word) {
  int i;

  fprintf(stream, "*** Word \"");
  for (i = 0 ; word[i] != '\0' ; i++) {
    putc(tolower(word[i]), stream);
  }
  fprintf(stream, "\" wasn't found\n");
}

void printInteractiveHelp(FILE *stream) {
    fprintf(stream, " - exits on an empty line\n");
    fprintf(stream, 
	    " - type %s to toggle between rhyme and syllable searches\n",
	    SWAPSYLLABLEKEY);
    fprintf(stream,
	    " - type %s to toggle between merged and non-merged results\n",
	    SWAPMERGEDKEY);
    fprintf(stream, " - type %s for help\n", HELPKEY);
}
