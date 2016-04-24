/**
 * @file   mmap.c
 * @author Wang Yuanxuan <zellux@gmail.com>
 * @date   Fri Jan  8 21:23:31 2010
 * 
 * @brief  An implementation of mmap bench mentioned in OSMark paper
 * 
 * 
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>

#include "config.h"
#include "bench.h"
#include "parameters.h"

#include "tracing.h"

int nbufs = NUM_PAGES_TO_TOUCH_MF;
char *shared_area = NULL;
char *filename = "share.dat";
int loopIter = NUM_TIMES_TO_RUN;

void worker(int warmUp)
{
    //printf("potato_test: In worker\n");
    volatile int ret = 0;
    volatile int i,j;	 


    int numTimesToRun = NUM_TIMES_TO_RUN;
    if (warmUp == 1)
	numTimesToRun=1;
    for (j=0; j<numTimesToRun;j++)
    {
    	for (i = 0; i < nbufs*4096; i++)
        	ret += shared_area[i];
    }
    //printf("potato_test: done\n");

}

int
main(int argc, char **argv)
{
    int fd;
    uint64_t start, end, nsec;
    printf("nbufs is %d\n",nbufs);
    #if (TRACE_MODE == 1)
    setup_trace();
    #endif

    if (argc > 1) {
        filename = argv[1];
    }
    printf("Filename is %s \n",filename);
    fd = open(filename, O_RDONLY);
    shared_area = mmap(NULL, (1 + nbufs) * 4096, PROT_READ, MAP_PRIVATE, fd, 0);
    if (shared_area == MAP_FAILED)
    {
	    printf("mmap call was not successful, shared_area pointer value is %p, error is %s\n",(void *)shared_area,strerror(errno));
	    exit(1);
    }
    affinity_set(1);   
 //   worker(1);
    start = read_tsc();
    setup_pf();
    start_pf_count();

    #if (TRACE_MODE == 1)
    //printf("Setting trace on\n");
    trace_on();
    #endif
    worker(0);

    #if (TRACE_MODE == 1)
    //printf("Setting trace off\n");
    trace_off();
    #endif
    end = read_tsc();
    nsec = (end - start) * 1000000 / get_cpu_freq();
    //printf("nsec: %ld\t\n", nsec/(NUM_TIMES_TO_RUN+1));
    printf("nsec: %ld\t\n", nsec/(NUM_TIMES_TO_RUN));
    end_pf_count();
    close(fd);
    return 0;
}
