#ifndef _TRACING_H_
#define _TRACING_H_

#include <stdio.h>
#include <stdlib.h>
//#define DEBUG

void setup_pf();
void get_pf(unsigned long*, unsigned long*);
void end_pf_count();

static int __pid;
static char procfile[40];
static unsigned long maj_flt_cnt, min_flt_cnt;

static int trace_fd;
void setup_trace()
{
    trace_fd = open("/sys/kernel/debug/tracing/tracing_on", O_WRONLY);
    printf("Writing to tracing_on file \n");
    if(trace_fd < 0)
      perror("Unable to start tracing");
    setup_pf();
}

void trace_on()
{
    if(trace_fd > 0)
    {
        if (write(trace_fd, "1", 1) != 1)
	{
		printf("[ERROR!!!!!!!!!] Write to tracing_on is not successful!\n");
	}
    }
    get_pf(&min_flt_cnt, &maj_flt_cnt);
}

void trace_off()
{
    end_pf_count();
    if(trace_fd > 0)
    {
        if (write(trace_fd, "0", 1) != 1)
	{
		printf("[ERROR!!!!!!!!!] Write to tracing_off is not successful!\n");
	}
    }
    //close(trace_fd);
}

/*-- Read page fault count from /proc/<pid> -*/

void setup_pf()
{
    __pid = getpid();
    sprintf(procfile, "/proc/%d/stat", __pid);
    // moved file open to get_pf()
}

void get_pf(unsigned long *min_flt, unsigned long *maj_flt)
{

    int pid;
    unsigned long cmaj, cmin;
    FILE* procf;

    char state;
    char comm[50];

#ifdef DEBUG
    printf("Opening proc file %s\n", procfile);
#endif
    procf = fopen(procfile, "r");
    if(procf == NULL)
      perror("Unable to opec proc file");

    char line[200];

    // get line
    if( fgets(line, sizeof(line), procf) < 0) {
        printf("Error reading proc file\n");
        return;
    }

    sscanf(line, "%d %s %c %*d %*d %*d %*d %*d %*u %lu %lu %lu %lu" ,
               //  1  2  3   4   5   6   7   8   9 [10]   [12]
                     &pid, comm, &state, 
                  //   &ppid, &pgid, &sid, &tty_nr, &tpgid, &flags,
                     min_flt, &cmin, maj_flt, &cmaj  );
#ifdef DEBUG
    printf(" Line read: %s\n", line);
    printf(" checking pid = %d , process = %s\n", pid, comm);
    printf(" minor faults %lu , major faults = %lu\n", *min_flt, *maj_flt);
#endif

    fclose(procf);
}

/*-- dumps pf count difference between last trace point and now */
void end_pf_count()
{
    unsigned long  new_maj_flt, new_min_flt;
    unsigned long  diff_maj_flt, diff_min_flt;

    get_pf(&new_min_flt, &new_maj_flt);

    diff_min_flt = new_min_flt - min_flt_cnt;
    diff_maj_flt = new_maj_flt - maj_flt_cnt;

    printf(" minor_pf = %lu,  major_pf = %lu\n", diff_min_flt, diff_maj_flt);
}
#endif
