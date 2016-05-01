#include <papi.h>

#define numEvents 1
//int events[numEvents] = {PAPI_RES_STL, PAPI_L2_DCA, PAPI_L3_DCA,  PAPI_TOT_INS, PAPI_TOT_CYC};//, PAPI_L3_DCM};//, PAPI_L1_DCA, PAPI_L2_DCA, PAPI_L3_DCA};
int events[numEvents] = {

PAPI_REF_CYC ,
};
// long_long dummy_values[numEvents];
long_long values[numEvents];

void print_counters()
{
    int i;
    for (i=0;i<numEvents;i++)
    {
        printf("%lld\n",values[i]);
    }
}

void check()
{
    if (PAPI_num_counters() < numEvents) {
           fprintf(stderr, "No hardware counters here, or PAPI not supported.\n");
              exit(1);
    }
}

void start_papi_counters()
{
    int ret;
    if ((ret = PAPI_start_counters(events, numEvents)) != PAPI_OK) {
           fprintf(stderr, "PAPI failed to start counters: %s\n", PAPI_strerror(ret));
              exit(1);
    }
    
}

void read_papi_counters()
{
    int ret;
    if ((ret = PAPI_read_counters(values, numEvents)) != PAPI_OK) {
          fprintf(stderr, "PAPI failed to read counters: %s\n", PAPI_strerror(ret));
           exit(1);
    }
    print_counters();
}

