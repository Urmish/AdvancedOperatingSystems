CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

default: mmapbench

forkbench: mmapbench.o
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -rf *.o
	rm -rf mmapbench
