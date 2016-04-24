#!/usr/bin/python

import os, re, sys
from subprocess import *
import shutil
import operator

NUM_TIMES_TO_RERUN_EXP=101
NUM_TIMES_TO_RUN=1
debug = 0;
flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
repeat = 1
files = ['/home/cs736/Documents/Tests/Data/random_3GB.img','/home/cs736/Documents/fs_tmpfs/random_3GB.img','/home/cs736/Documents/fs_pmfs/random_3GB.img']
fsType = ['ext4','tmpfs','pmfs']
pages = [1,2,16,64,256,1024,4192,16768,128000]
numFs = 3
valuesTime = [[],[],[]]
valuesPageFaults = [[],[],[]]
valuesMajorPageFaults = [[],[],[]]
valuesMinorPageFaults = [[],[],[]]
patterns = ['cache-references','cache-misses','L1-dcache-loads','L1-dcache-load-misses','L1-dcache-stores','L1-dcache-store-misses','L1-dcache-prefetches','L1-dcache-prefetch-misses','L1-icache-loads','L1-icache-load-misses','LLC-loads','LLC-load-misses','LLC-stores','LLC-store-misses','LLC-prefetches','LLC-prefetch-misses','dTLB-loads','dTLB-load-misses','dTLB-stores','dTLB-store-misses','iTLB-loads','iTLB-load-misses']
perfPatterns = {'ext4':{}, 'tmpfs':{}, 'pmfs':{}};

patternsHitRatio = ['L1-dcache-load','L1-dcache-store','L1-icache-load','LLC-load','LLC-store','dTLB-load','dTLB-store','iTLB-load']

def median(lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2
        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

def warmup():
        if debug==1:
    	    print('Warming up...')
	for i in xrange(3):
		p = Popen('./mmapcall 1', shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)

def build(page=1):
  p = Popen("make clean",shell=True,stdout=PIPE)
  #cmd = "make -B MMAP_FLAG='%s'" % flag
  os.waitpid(p.pid, 0)
  cmd = "make -B NUM_PAGES_TO_TOUCH_MF="+str(page)+" NUM_TIMES_TO_RUN="+str(NUM_TIMES_TO_RUN)
  if debug==1:
    print cmd
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def flush():
  #print "Cache flush"
  cmd = "free > /dev/null && sync && echo 3 > /proc/sys/vm/drop_caches && free > /dev/null"
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def test():
        if debug==1:
	    print('Begin testing...')
	pattern = re.compile(r'nsec: (\d+)')
	pattern2 = re.compile(r'minor_pf = (\d+),  major_pf = (\d+)')
	count = 0
	for i in files:
		#print './mmapcall %s %s' % (base, numfiles)
                timeAcrossRuns = []
                minorfAcrossRuns = []
                majorfAcrossRuns = []
                for runC in xrange(NUM_TIMES_TO_RERUN_EXP):
		    flush()
		    p = Popen('$PWD/mmapbench.out '+i , shell=True,stdout=PIPE)
      		    os.waitpid(p.pid, 0)
		    output = p.stdout.read().strip()
		    usec = int(pattern.search(output).group(1))
		    minor_pf = int(pattern2.search(output).group(1))
		    major_pf = int(pattern2.search(output).group(2))
                    if debug==1:
		        print "Time - "+ str(usec)
		        print "minor_pf - "+str(minor_pf)
		        print "major_pf - "+str(major_pf)
                    timeAcrossRuns.append(usec)
                    minorfAcrossRuns.append(minor_pf)
                    majorfAcrossRuns.append(major_pf)
                print fsType[count]
                print 'time'+',' +  ','.join(str(e) for e in timeAcrossRuns)
                print 'major fauts'+',' +  ','.join(str(e) for e in majorfAcrossRuns)
                print 'minor faults'+',' +  ','.join(str(e) for e in minorfAcrossRuns)
		valuesTime[count].append(median(timeAcrossRuns))
		valuesMajorPageFaults[count].append(median(majorfAcrossRuns))
		valuesMinorPageFaults[count].append(median(minorfAcrossRuns))
		count=count+1

def testTrace(page):
        if debug==1:
    	    print('Begin testing...')
	pattern = re.compile(r'minor_pf = (\d+),  major_pf = (\d+)')
	#total = 0
	for i in xrange(numFs):
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('/home/cs736/Documents/Tests/Tests/FtraceScripts/traceprocess.sh $PWD/mmapbench_trace.out '+files[i] , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		minor_pf = int(pattern.search(output).group(1))
		major_pf = int(pattern.search(output).group(2))
                if debug==1:
		    print "minor_pf "+str(minor_pf)
		    print "major_pf "+str(major_pf)
		shutil.rmtree("trace_"+fsType[i]+"_"+str(page), ignore_errors=True)
		os.rename("trace", "trace_"+fsType[i]+"_"+str(page))
		output = p.stdout.read().strip()
		valuesMajorPageFaults[i].append(major_pf)
		valuesMinorPageFaults[i].append(minor_pf)

def testPerf():
        if debug==1:
	    print('Begin Perf...')
	total = 0
	count = 0
	for i in files:
		flush()
		p = Popen('~/bin/perf stat -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-dcache-store-misses,L1-dcache-prefetches,L1-dcache-prefetch-misses,L1-icache-loads,L1-icache-load-misses,LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses,LLC-prefetches,LLC-prefetch-misses,dTLB-loads,dTLB-load-misses,dTLB-stores,dTLB-store-misses,iTLB-loads,iTLB-load-misses -o perf.log $PWD/mmapbench.out $PWD/'+i+' ' , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		textfile = open('perf.log', 'r')
		filetext = textfile.read()
		textfile.close()
                if debug==1:
		    print 'perf.log is '
		    print filetext
		for getPattern in patterns:
			pattern = re.compile(r'(\d+.*) '+getPattern)
			tempVar = 0
			if (pattern.search(filetext)):
				tempVar = pattern.search(filetext).group(1)
				tempVar = tempVar.replace(',','')
				tempVar = int(tempVar)
                        if debug==1:
			    print getPattern+" "+ str(tempVar)
			if getPattern in perfPatterns[fsType[count]]:
				perfPatterns[fsType[count]][getPattern].append(tempVar)
			else:
				perfPatterns[fsType[count]][getPattern] = [tempVar]
		count=count+1

NUM_TIMES_TO_RERUN_EXP=int(sys.argv[1])
NUM_TIMES_TO_RUN=int(sys.argv[2])
print "Current Working Directory -"+os.getcwd()
print "Num Times to rerun exp -"+str(NUM_TIMES_TO_RERUN_EXP)
print "Num Times to run within code -"+str(NUM_TIMES_TO_RUN)

csvDat = open("mmapbench_"+str(NUM_TIMES_TO_RERUN_EXP)+".csv",'w')

for page in pages:
	print "Running for num pages = "+str(page)
	build(page)
	test()
	#testTrace(page)
	testPerf()
line="Pages"
for page in pages:
    line=line+','+str(page)

csvDat.write("\n")
csvDat.write("Time")
csvDat.write("\n")
csvDat.write(line)
csvDat.write("\n")
csvDat.write("malloc,")
csvDat.write("\n")
for i in xrange(3):
	csvDat.write(fsType[i]+',' + ','.join(str(e) for e in valuesTime[i]))
        csvDat.write("\n")


csvDat.write("\n")
csvDat.write("MajorPageFaults")
csvDat.write("\n")
csvDat.write(line)
csvDat.write("\n")
csvDat.write("malloc,")
csvDat.write("\n")
for i in xrange(3):
	csvDat.write(fsType[i]+',' +  ','.join(str(e) for e in valuesMajorPageFaults[i]))
        csvDat.write("\n")

csvDat.write("\n")
csvDat.write("MinorPageFaults")
csvDat.write("n")
csvDat.write(line)
csvDat.write("\n")
csvDat.write("malloc,")
csvDat.write("\n")
for i in xrange(3):
	csvDat.write(fsType[i]+',' +  ','.join(str(e) for e in valuesMinorPageFaults[i]))
        csvDat.write("\n")

for getPattern in patterns:
	csvDat.write("\n")
	csvDat.write(getPattern)
	csvDat.write("\n")
	csvDat.write(line)
        csvDat.write("\n")
        csvDat.write("malloc,")
        csvDat.write("\n")
	for i in xrange(3):
		csvDat.write(fsType[i]+',' +  ','.join(str(e) for e in perfPatterns[fsType[i]][getPattern]))
                csvDat.write("\n")

for getPattern in patternsHitRatio:
	csvDat.write("\n")
	csvDat.write(getPattern+' Hit Ratio')
	csvDat.write("\n")
	csvDat.write(line)
        csvDat.write("\n")
        csvDat.write("malloc,")
        csvDat.write("\n")
	for i in xrange(3):
		ratioDenominator = perfPatterns[fsType[i]][getPattern+'s']
		ratioNumerator =  perfPatterns[fsType[i]][getPattern+'-misses'] #Miss Ratio
		ratioNumerator = map(operator.sub, ratioDenominator,ratioNumerator)
		ratio = []
		for j in xrange(len(ratioNumerator)):
			if (ratioDenominator[j] == 0):
				ratio.append('NA')
			else:
				ratio.append(float(float(ratioNumerator[j])/float(ratioDenominator[j])))
		csvDat.write(fsType[i]+',' +  ','.join(str(e) for e in ratio))
                csvDat.write("\n")
csvDat.close()
