CC=gcc
CFLAGS=-O2 -Wall -pthread -I ../include

MMAP_FLAG=MAP_PRIVATE|MAP_ANONYMOUS
PROT_FLAG=PROT_READ

CDEFINES= -DMMAP_FLAG='$(MMAP_FLAG)' -DMY_PROT_FLAG='$(PROT_FLAG)'

default: mmapcall.out mmapcall_trace.out

mmapcall.out: mmapcall.c
	$(CC) -o mmapcall.out -DTRACE_MODE=0 $^ $(CFLAGS) $(CDEFINES)

mmapcall_trace.out: mmapcall.c
	$(CC) -o mmapcall_trace.out -DTRACE_MODE=1 $^ $(CFLAGS) $(CDEFINES)

clean:
	rm -rf *.o
	rm -rf mmapcall
	rm -rf mmapcall.out
