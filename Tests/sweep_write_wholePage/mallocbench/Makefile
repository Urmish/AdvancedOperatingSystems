CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../../../Tests/Tests/include
NUM_PAGES_TO_TOUCH_MF=1
NUM_TIMES_TO_RUN=1000
default: mallocbench.out

mallocbench.out:	mallocbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=0 -DNUM_PAGES_TO_TOUCH_MF='$(NUM_PAGES_TO_TOUCH_MF)' -DNUM_TIMES_TO_RUN='$(NUM_TIMES_TO_RUN)' -o mallocbench.out mallocbench.c
	$(CC) $(CFLAGS) -DTRACE_MODE=1 -DNUM_PAGES_TO_TOUCH_MF='$(NUM_PAGES_TO_TOUCH_MF)' -DNUM_TIMES_TO_RUN='$(NUM_TIMES_TO_RUN)' -o mallocbench_trace.out mallocbench.c 

clean:
	rm -rf *.o
	rm -rf mallocbench
	rm -rf mallocbench.out
	rm -rf mallocbench_trace.out
