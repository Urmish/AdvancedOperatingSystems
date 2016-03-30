CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

default: mmapbench.out

mmapbench.out:	mmapbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=0 -o mmapbench.out mmapbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=1 -o mmapbench_trace.out mmapbench.c
	

clean:
	rm -rf *.o
	rm -rf mmapbench.out
	rm -rf mmapbench_trace.out
