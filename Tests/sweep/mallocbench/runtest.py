#!/usr/bin/python

import os, re, sys
from subprocess import *
import shutil

flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
pages = [1,4,16,64,256,1024,4192,16768,128000]
repeat = 1
files = ['../../../Data/random.img','../../../../fs_tmpfs/random.img','../../../../fs_pmfs/random.img']
fsType = ['malloc']
numFs = 1
valuesTime = []
valuesPageFaults = []
valuesMajorPageFaults = []
valuesMinorPageFaults = []

def warmup():
	print('Warming up...')
	for i in xrange(3):
		p = Popen('./mmapcall 1', shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)

def build(page=1):
  p = Popen("make clean",shell=True)
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
	flush()
	p = Popen('$PWD/mallocbench.out ', shell=True, stdout=PIPE)
	os.waitpid(p.pid, 0)
	output = p.stdout.read().strip()
	usec = int(pattern.search(output).group(1))
	print usec
	valuesTime.append(usec)
	total += usec
	#print('Average: %d' % ( total / repeat))

def testTrace(page):
	pattern = re.compile(r'minor_pf = (\d+),  major_pf = (\d+)')
	for i in xrange(numFs):
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('$PWD/mallocbench_trace.out $PWD/'+files[i] , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		minor_pf = int(pattern.search(output).group(1))
		major_pf = int(pattern.search(output).group(2))
		print "minor_pf "+str(minor_pf)
		print "major_pf "+str(major_pf)
		valuesMajorPageFaults.append(major_pf)
		valuesMinorPageFaults.append(minor_pf)


for page in pages:
	print "Building.."
	build(page)
	test()
	testTrace(page)
print pages
print valuesTime
#print valuesPageFaults
print valuesMajorPageFaults
print valuesMinorPageFaults
