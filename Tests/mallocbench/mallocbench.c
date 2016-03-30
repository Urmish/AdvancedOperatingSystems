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

#include "config.h"
#include "bench.h"
#include "parameters.h"
//#include "tracing.h"

int nbufs = NUM_PAGES_TO_TOUCH;
char *shared_area = NULL;
char *filename = "share.dat";

void worker()
{
    volatile int ret = 0;
    int i;

    for (i = 0; i < nbufs; i++)
        ret += shared_area[i *4096];
    //printf("potato_test: thread#%d done.\n", core);
}

int
main(int argc, char **argv)
{
    uint64_t start, end, nsec;


    //if (argc > 1) {
    //    filename = argv[1];
    //}
    //printf("Filename is %s \n",filename);
    //fd = open(filename, O_RDONLY);
    //setup_trace();
    shared_area = (char *)malloc((1 + nbufs) * 4096);
    affinity_set(1);   
    start = read_tsc();

    //trace_on();
    worker();
    //trace_off();

    end = read_tsc();
    nsec = (end - start) * 1000 / get_cpu_freq();
    printf("nsec: %ld\t\n", nsec);

    //close(fd);
    return 0;
}
