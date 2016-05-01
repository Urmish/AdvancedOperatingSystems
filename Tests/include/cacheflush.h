
int flush_cache(int cache_size) //Size in MB
{
    const int size = cache_size*1024*1024; // Allocate 20M. Set much larger then L2
    int i,j;
    int sum=0;
    char *c = (char *)malloc(size);
    for (i = 0; i < 0xffff; i++)
        for (j = 0; j < size; j++)
        {
            c[j] = i*j;
            sum+=c[j];
        }   
    free(c);
    return sum;
}
