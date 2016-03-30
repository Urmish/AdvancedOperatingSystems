CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

MMAP_FLAG=MAP_PRIVATE

CDEFINES= -DMMAP_FLAG='$(MMAP_FLAG)'
CFLAGS+=$(CDEFINES)

default: mmapcall.out

mmapcall.out: mmapcall.c
	$(CC) -o mmapcall.out $^ $(CFLAGS) $(CDEFINES)

clean:
	rm -rf *.o
	rm -rf mmapcall
	rm -rf mmapcall.out
