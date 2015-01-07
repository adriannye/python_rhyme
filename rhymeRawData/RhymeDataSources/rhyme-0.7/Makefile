CC = gcc
INCLUDES = -I/usr/include/readline
LIBS = -lgdbm -lreadline -ltermcap
FLAGS = -Wall -O

TEXTFILES = words.txt rhymes.txt multiple.txt
DBFILES = words.db rhymes.db multiple.db
MAKEDBSARGS = $(TEXTFILES) compile.c

RHYMEPATH = /usr/share/rhyme
BINPATH = /usr/bin

all: compile words.db rhymes.db multiple.db rhyme

install: all
	install --mode=755 rhyme $(BINPATH)
	install --mode=755 -d $(RHYMEPATH)
	install --mode=644 words.db $(RHYMEPATH)
	install --mode=644 rhymes.db $(RHYMEPATH)
	install --mode=644 multiple.db $(RHYMEPATH)

uninstall:
	rm -f $(BINPATH)/rhyme
	rm -rf $(RHYMEPATH)

clean:
	rm -f rhyme compile *.o $(DBFILES)

cleanall: clean
	rm -f $(MAKEDBSARGS)

compile.c: cmudict.0.6-1 cmudict.patch
	python merge.py cmudict.0.6-1 cmudict.patch | \
python makedbs.py $(MAKEDBSARGS)

compile: compile.c
	$(CC) $(FLAGS) -o compile compile.c -lgdbm

words.txt: cmudict.0.6-1 cmudict.patch
	python merge.py cmudict.0.6-1 cmudict.patch | \
python makedbs.py $(MAKEDBSARGS)

rhymes.txt: cmudict.0.6-1 cmudict.patch
	python merge.py cmudict.0.6-1 cmudict.patch | \
python makedbs.py $(MAKEDBSARGS)

multiple.txt: cmudict.0.6-1 cmudict.patch
	python merge.py cmudict.0.6-1 cmudict.patch | \
python makedbs.py $(MAKEDBSARGS)

words.db: words.txt compile
	./compile words.txt words.db

rhymes.db: rhymes.txt compile
	./compile rhymes.txt rhymes.db

multiple.db: multiple.txt compile
	./compile multiple.txt multiple.db

setup.o: setup.h setup.c
	$(CC) $(FLAGS) -c setup.c $(INCLUDES) -DDEFAULT_RHYMEPATH="\"$(RHYMEPATH)\""

getopt.o: getopt.c getopt.h
	$(CC) $(FLAGS) -c getopt.c

getopt1.o: getopt1.c getopt.h
	$(CC) $(FLAGS) -c getopt1.c

rhyme.o: rhyme.h rhyme.c
	$(CC) $(FLAGS) -c rhyme.c $(INCLUDES)

rhyme: rhyme.o setup.o getopt1.o getopt.o
	$(CC) $(FLAGS) -o rhyme rhyme.o setup.o getopt1.o getopt.o $(LIBS)
