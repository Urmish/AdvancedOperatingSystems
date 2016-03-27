#!/bin/sh

base=$1
max=$(expr $2 - 1)

for i in `seq 0 $max` 
do
  dd if=/dev/urandom of=$base$i bs=1M count=1
done

# dd if=/dev/urandom of=share.dat bs=1M count=500
