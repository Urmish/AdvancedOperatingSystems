CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

default: mmapcall

forkbench: mmapcall.o
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -rf *.o
	rm -rf mmapcall
