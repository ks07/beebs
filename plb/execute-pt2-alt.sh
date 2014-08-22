#!/bin/bash

if [ -z "$TIMEOUT" ]; then
    TIMEOUT=15
fi

# Repeat the tests 3 times
for i in {1..3}; do

    echo "name,energy,time,avg_power,avg_current,avg_voltage" > "energy.csv.$i" 

    BENCHES=$(find src/ -type f -executable -not -name "template" -printf "%f:%p\n")

    for bline in $BENCHES; do
	bn=$(echo "$bline" | cut -d ':' -f 1)
	bp=$(echo "$bline" | cut -d ':' -f 2)

	nrg=$(timeout "$TIMEOUT" platformrun --csv atmega328p "$bp")
	
	if [[ "$?" -eq "0" ]]; then
	    nrg=$(echo "$nrg" | sed 's/, //g')
	else
	    nrg="0,0,0,0,0"
	fi

	echo "${bn},${nrg}" >> "energy.csv.$i"
    done
done
