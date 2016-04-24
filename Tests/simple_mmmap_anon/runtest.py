#!/usr/bin/python

import os, re, sys
from subprocess import *

corelist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#flags = ['MAP_PRIVATE', 'MAP_SHARED', 'MAP_PRIVATE|MAP_POPULATE', 'MAP_SHARED|MAP_POPULATE']
#flags = ['MAP_ANONYMOUS|MAP_PRIVATE|MAP_POPULATE', 'MAP_ANONYMOUS|MAP_SHARED|MAP_POPULATE']
flags = ['MAP_ANONYMOUS|MAP_PRIVATE', 'MAP_ANONYMOUS|MAP_SHARED']
pages = [1, 4, 16, 64, 256, 1024, 4096, 16384]#, 128000]
#pages = [4096]
repeat = 10 

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

def test(pages, numcalls):
	print('Begin testing...')
	pattern = re.compile(r'nsec: (\d+)')
	total = 0
	for i in xrange(repeat):
		flush()
		print './mmapcall.out %d %s' % (pages, numcalls)
		p = Popen('./mmapcall.out %d %s' % (pages, numcalls), shell=True, stdout=PIPE)
		os.waitpid(p.pid, 0)
		output = p.stdout.read().strip()
		usec = int(pattern.search(output).group(1))
		print usec
		total += usec
        print('Pages: %d , Average: %d' % ( pages, total / repeat))

#warmup()
numcalls = sys.argv[1]

for flag in flags:
	print "\n\n============================================"
	print "Flag = ", flag
	print "Building.."
	print "\n\n============================================"
	build(flag)
	for page in pages:
		print "Testing page size =%d, flag = %s" %(page, flag)
		test(page, numcalls)
