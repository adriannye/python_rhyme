#include <stdio.h>
#include <gdbm.h>
#include <stdlib.h>

/*This value is precalculated from the makedbs.py file.
  If the raw dictionary files are changed, this source file will be
  re-generated automatically.*/
#define MAX_LINE 9795

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
	    "*** Usage: compile <text input file> <gdbm output file>\n");
    exit(1);
  }

  input = fopen(argv[1], "r");

  if (input == NULL) {
    fprintf(stderr,
	    "error opening %s\n", argv[1]);
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
    key[i] = '\0';

    for (j=0; (inputline[i] != '\n') && (inputline[i] != '\0'); i++,j++) {
      value[j] = inputline[i];
      valuesize++;
    }

    value[j] = '\0';

    keyd.dsize = keysize;
    valued.dsize = valuesize;

    if (gdbm_store(output, keyd, valued, GDBM_INSERT) == 1) {
      fprintf(stderr, "Key %s is already present in database\n", key);
      exit(1);
    }

    lines++;
  }

  gdbm_sync(output);

  fclose(input);
  gdbm_close(output);

  printf("Inserted %d lines into %s\n", lines, argv[2]);

  return 0;
}
