CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

MMAP_FLAG=MAP_PRIVATE

CDEFINES= -DMMAP_FLAG='$(MMAP_FLAG)'
CFLAGS+=$(CDEFINES)

default: mmapcall

forkbench: mmapcall.o
	$(CC) -o $@ $^ $(CFLAGS) $(CDEFINES)

clean:
	rm -rf *.o
	rm -rf mmapcall
