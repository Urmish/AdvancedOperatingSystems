#!/usr/bin/python

import os, re, sys
from subprocess import *
import shutil

flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
repeat = 1
files = ['../../Data/random.img','../../../fs_tmpfs/random.img','../../../fs_pmfs/random.img']
fsType = ['ext4','tmpfs','pmfs']
numFs = 3

def warmup():
	print('Warming up...')
	for i in xrange(3):
		p = Popen('./mmapcall 1', shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)

def build(flag='MAP_PRIVATE'):
  #cmd = "make -B MMAP_FLAG='%s'" % flag
  cmd = "make"
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
	for i in files:
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('$PWD/mmapbench.out '+i , shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		usec = int(pattern.search(output).group(1))
		print usec
		total += usec
	print('Average: %d' % ( total / repeat))

def testTrace():
	print('Begin testing...')
	pattern = re.compile(r'nsec: (\d+)')
	#total = 0
	for i in xrange(numFs):
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('../FtraceScripts/traceprocess.sh $PWD/mmapbench_trace.out $PWD/'+files[i] , shell=True,stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		#usec = int(pattern.search(output).group(1))
		#print usec
		#total += usec
		shutil.rmtree("trace_"+fsType[i], ignore_errors=True)
		os.rename("trace", "trace_"+fsType[i])
	#print('Average: %d' % ( total / repeat))



print "Building.."
build()
test()
testTrace()
