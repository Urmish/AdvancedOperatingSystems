#!/bin/bash
 
DPATH="/sys/kernel/debug/tracing"
PID=$$
## Quick basic checks
[ `id -u` -ne 0  ]  &&  { echo "needs to be root" ; exit 1; }  # check for root permissions
[ -z $1 ] && { echo "needs process name as argument" ; exit 1; } # check for args to this function
mount | grep -i debugfs &> /dev/null
[ $? -ne 0 ] && { echo "debugfs not mounted, mount it first"; exit 1; } #checks for debugfs mount

declare -a available_tracers=("function_graph" "function" "blk")

declare -a trace_options=("print-parent" "nosym-offset" "nosym-addr" "noverbose" "noraw" "nohex" "nobin" "noblock" "nostacktrace" "trace_printk" "noftrace_preempt" "nobranch" "annotate" "nouserstacktrace" "nosym-userobj" "noprintk-msg-only" "context-info" "nolatency-format" "sleep-time" "graph-time" "record-cmd" "overwrite" "nodisable_on_free" "irq-info" "markers" "function-trace" "nofunc_stack_trace")

if [ ! -d "$DIRECTORY" ]
then
  mkdir trace
else
  rm -rf trace/*
fi

for i in "${available_tracers[@]}"
do
	# flush existing trace data
	echo nop > $DPATH/current_tracer
 
	printStatement="Tracing based on following option "$i
	echo $printStatement 

	# set function tracer
	echo $i > $DPATH/current_tracer
 
	# enable the current tracer
	#echo 1 > $DPATH/tracing_enabled
	# write current process id to set_ftrace_pid file
	echo $PID > $DPATH/set_ftrace_pid
 
	# start the tracing
	echo 1 > $DPATH/tracing_on
	# execute the process
	$*

	cp /sys/kernel/debug/tracing/trace trace/$i\.log
done
:> $DPATH/set_ftrace_pid
