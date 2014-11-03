#!/bin/bash


###
# Print text based progress bar
#
# param 1 - length of bar in chars
# param 2 - percentage value
###
update_progress_bar() {
    percent=$((${2}))
    bar_length=$((${1}))
    bar_chr="#"
    bar_line=""
	
    num_chrs=$(($bar_length*$percent/100+1))
    for i in $(seq 1 ${bar_length}); do
		if [ $i -lt $num_chrs ]; then
        	bar_line="${bar_line}="
		else
			bar_line="${bar_line}."
		fi
    done
    
    printf "|${bar_line}|  (${percent}%%)\r"
}


#EXAMPLE
for n in $(seq 10 100); do
	update_progress_bar 40 $n
	sleep 1
done

