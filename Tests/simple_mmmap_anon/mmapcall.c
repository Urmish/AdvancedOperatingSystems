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

#if (TRACE_MODE == 1)
#include "tracing.h"
#endif

//int nbufs = NUM_PAGES_TO_TOUCH;
int nbufs = 255;
char *shared_area = NULL;
uint64_t *measurements;

void usage()
{
  printf(
  "Usage: ./mmapcall <num_pages_tomap> <numcalls> \n"
  ""
  "   ./mmapcall 1024 100 \n"
  " will will do 100 an anonymous mmap calls 1024 pages each\n");
  exit(-1);
}

void print_measurements(uint64_t* marray, int size)
{
  int i;
  printf("Meaurements = \n");
  for(i = 0; i < size; i++) {
    printf("%ld\n", marray[i]);
  }
}

uint64_t stat_average(uint64_t* marray, int size)
{
  uint64_t sum = 0;
  int i;
  for(i = 0; i < size; i++) {
    sum += marray[i];
  }
  return sum/(uint64_t)size;
}

int
main(int argc, char **argv)
{
    int numcalls, i;
    uint64_t start, end, nsec;

    if (argc > 2) {
        nbufs = atoi(argv[1]);
        numcalls = atoi(argv[2]);
    }
    else
      usage();

    measurements = (uint64_t*) malloc(numcalls * sizeof(uint64_t));
    affinity_set(1);   

    #if (TRACE_MODE == 1)
    setup_trace();
    #endif

    for(i=0; i < numcalls; i++) {
      #if (TRACE_MODE == 1)
      trace_on();
      #endif

      start = read_tsc();
      shared_area = mmap(0, (1 + nbufs) * 4096, MY_PROT_FLAG, MMAP_FLAG, -1 , 0);
      end = read_tsc();

      #if (TRACE_MODE == 1)
      trace_off();
      #endif

      if(shared_area == NULL) {
          fprintf(stderr, "mmap call failed\n");
          exit(1);
      }
      measurements[i] = end - start;
      //printf("measured %ld\n", end -start);
    }

    print_measurements(measurements, numcalls);
    nsec = stat_average(measurements, numcalls) * 1000000000 / get_cpu_freq();
    printf("nsec: %ld\t\n", nsec);

    return 0;
}
