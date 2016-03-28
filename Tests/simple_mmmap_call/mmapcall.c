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

//int nbufs = NUM_PAGES_TO_TOUCH;
int nbufs = 255;
char *shared_area = NULL;
char *filebase = "files";
uint64_t *measurements;

void usage()
{
  printf(
  "Usage: ./mmapcall <filename_base> <numfiles> \n"
  ""
  " note that filename base specifies the prefix for mmaped files, for ex -\n"
  "   ./mmapcall ./data/files 100 \n"
  " will access ./data/files0 through ./data/files99\n");
  exit(-1);
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
    int fd, numfd, i;
    uint64_t start, end, nsec;
    char filename[1024];

    if (argc > 2) {
        filebase = argv[1];
        numfd = atoi(argv[2]);
    }
    else
      usage();

    printf("Filename base is %s \n",filebase);
    measurements = (uint64_t*) malloc(numfd * sizeof(uint64_t));
    affinity_set(1);   

    for(i=0; i < numfd; i++) {
      snprintf(filename, 1024, "%s%d", filebase, i);
      fd = open(filename, O_RDONLY);

      start = read_tsc();
      shared_area = mmap(0, (1 + nbufs) * 4096, PROT_READ, MMAP_FLAG, fd, 0);
      end = read_tsc();

      measurements[i] = end - start;
      //printf("measured %ld\n", end -start);
      close(fd); // closing the file does not unmap the region
    }

    nsec = stat_average(measurements, numfd) * 1000000000 / get_cpu_freq();
    printf("nsec: %ld\t\n", nsec);

    return 0;
}
