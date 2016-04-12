#!/usr/bin/python

import os, re, sys
from subprocess import *
import shutil

flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
repeat = 1
files = ['../../../Tests/Data/random_3GB.img','../../../fs_tmpfs/random_3GB.img','../../../fs_pmfs/random_3GB.img']
fsType = ['ext4','tmpfs','pmfs']
pages = [1,4,16,64,256,1024,4192,16768,128000]
numFs = 3
valuesTime = [[],[],[]]
valuesPageFaults = [[],[],[]]
valuesMajorPageFaults = [[],[],[]]
valuesMinorPageFaults = [[],[],[]]

def warmup():
	print('Warming up...')
	for i in xrange(3):
		p = Popen('./mmapcall 1', shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)

def build(page=1):
  p = Popen("make clean",shell=True)
  #cmd = "make -B MMAP_FLAG='%s'" % flag
  os.waitpid(p.pid, 0)
  cmd = "make -B NUM_PAGES_TO_TOUCH_MF=%d" % page
  print cmd
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def flush():
  #print "Cache flush"
  cmd = "free > /dev/null && sync && echo 3 > /proc/sys/vm/drop_caches && free > /dev/null"
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def test():
	print('Begin testing...')
	pattern = re.compile(r'nsec: (\d+)')
	total = 0
	count = 0
	for i in files:
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('$PWD/mmapbench.out '+i , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		usec = int(pattern.search(output).group(1))
		print usec
		total += usec
		valuesTime[count].append(usec)
		count=count+1

def testTrace(page):
	print('Begin testing...')
	pattern = re.compile(r'minor_pf = (\d+),  major_pf = (\d+)')
	#total = 0
	for i in xrange(numFs):
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('$PWD/mmapbench_trace.out $PWD/'+files[i] , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		minor_pf = int(pattern.search(output).group(1))
		major_pf = int(pattern.search(output).group(2))
		print "minor_pf "+str(minor_pf)
		print "major_pf "+str(major_pf)
		#total += usec
		#shutil.rmtree("trace_"+fsType[i]+"_"+str(page), ignore_errors=True)
		#os.rename("trace", "trace_"+fsType[i]+"_"+str(page))
		#p = Popen('grep -ir "__do_page_fault()" trace_'+fsType[i]+'_'+ str(page) +'|wc -l',shell=True,stdout=PIPE)
		#os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		#valuesPageFaults[i].append(output)
		valuesMajorPageFaults[i].append(major_pf)
		valuesMinorPageFaults[i].append(minor_pf)
	#print('Average: %d' % ( total / repeat))


for page in pages:
	print "Building.."
	build(page)
	test()
	testTrace(page)
for i in xrange(3):
	print fsType[i]
	print pages
	print valuesTime[i]
	print valuesMajorPageFaults[i]
	print valuesMinorPageFaults[i]