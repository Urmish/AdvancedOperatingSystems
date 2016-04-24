CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../../../Tests/Tests/include
NUM_PAGES_TO_TOUCH_MF=128000
NUM_TIMES_TO_RUN=1000

default: mmapbench.out

mmapbench.out:	mmapbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=0 -DNUM_PAGES_TO_TOUCH_MF='$(NUM_PAGES_TO_TOUCH_MF)' -DNUM_TIMES_TO_RUN='$(NUM_TIMES_TO_RUN)' -o mmapbench.out mmapbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=1 -DNUM_PAGES_TO_TOUCH_MF='$(NUM_PAGES_TO_TOUCH_MF)' -DNUM_TIMES_TO_RUN='$(NUM_TIMES_TO_RUN)' -o mmapbench_trace.out mmapbench.c
	

clean:
	rm -rf *.o
	rm -rf mmapbench.out
	rm -rf mmapbench_trace.out
