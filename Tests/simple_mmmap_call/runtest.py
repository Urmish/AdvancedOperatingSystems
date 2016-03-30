#!/usr/bin/python

import os, re, sys
from subprocess import *

corelist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
repeat = 100 

def warmup():
	print('Warming up...')
	for i in xrange(3):
		p = Popen('./mmapcall 1', shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)

def build(flag='MAP_PRIVATE'):
  cmd = "make -B MMAP_FLAG='%s'" % flag
  print cmd
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def flush():
  #print "Cache flush"
  cmd = "free > /dev/null && sync && echo 3 > /proc/sys/vm/drop_caches && free > /dev/null"
  p = Popen(cmd,shell=True)
  os.waitpid(p.pid, 0)

def test(base, numfiles):
	print('Begin testing...')
	pattern = re.compile(r'nsec: (\d+)')
	total = 0
	for i in xrange(repeat):
		flush()
		#print './mmapcall %s %s' % (base, numfiles)
		p = Popen('./mmapcall %s %s' % (base, numfiles), shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		usec = int(pattern.search(output).group(1))
		#print usec
		total += usec
	print('Average: %d' % ( total / repeat))

#warmup()
basepath = sys.argv[1]
numfiles = sys.argv[2]

for flag in flags:
	print "Building.."
	build(flag)
	test(basepath, numfiles)
