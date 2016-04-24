#!/bin/bash
FILES=/home/cs736/Documents/urmish_work/sweep_write/mallocbench/trace_*
for f in $FILES
do
	i=`awk 'FNR > 4 { sum += $2; n++ } END { if (n > 0) print sum; }' $f"/function_graph.log"`
	j=`awk 'FNR > 4 { sum += $2; n++ } END { if (n > 0) print n; }' $f"/function_graph.log"`
	#echo $f"/function_graph.log" - $i
	echo $f"/function_graph.log" - $j
done
