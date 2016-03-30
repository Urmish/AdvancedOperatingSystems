#ifndef _TRACING_H_
#define _TRACING_H_

#include <stdio.h>
#include <stdlib.h>

static int trace_fd;
void setup_trace()
{
    trace_fd = open("/sys/kernel/debug/tracing/tracing_on", O_WRONLY);
    if(trace_fd < 0)
      perror("Unable to start tracing");
}

void trace_on()
{
    if(trace_fd > 0)
        write(trace_fd, "1", 1);
}

void trace_off()
{
    if(trace_fd > 0)
        write(trace_fd, "0", 1);
    //close(trace_fd);
}

#endif
