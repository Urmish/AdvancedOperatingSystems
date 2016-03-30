CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

default: mallocbench.out

mallocbench.out:	mallocbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=0 -o mallocbench.out mallocbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=1 -o mallocbench_trace.out mallocbench.c

clean:
	rm -rf *.o
	rm -rf mallocbench
	rm -rf mallocbench.out
