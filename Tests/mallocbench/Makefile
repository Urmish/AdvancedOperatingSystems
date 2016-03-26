CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

default: mallocbench

forkbench: mallocbench.o
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -rf *.o
	rm -rf mallocbnech
