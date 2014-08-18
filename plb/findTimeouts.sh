#!/bin/bash

RDIR=$(pwd -P)
NRGD=$(find . -maxdepth 2 -name 'energy.csv*' -size +0 -printf '%h\n' | grep './run-..*' | sort | uniq)

for d in $NRGD; do
    cd "$d" &&
    # Looks for tests in an energy.csv that have timed out, and attempts to re-run them.
    TMOUT=$(grep -x '.*,0,0,0,0,0' energy.csv* | sed 's/,0,0,0,0,0//')

    # Make some backups before we start modifying files
    find . -maxdepth 1 -name 'energy.csv*' -size +0 -exec cp {} {}.bkp \;

    for tst in $TMOUT; do
	NFILE=$(echo "$tst" | cut -d ':' -f 1)
	BMARK=$(echo "$tst" | cut -d ':' -f 2)

	if [ -f "src/$BMARK/$BMARK" ]; then
	    echo "Re-running $BMARK in $NFILE in $d"
	    OUT=$(platformrun --csv atmega328p "src/$BMARK/$BMARK" | sed 's/, /,/g')
	    OUT="${BMARK},${OUT}"
	    echo "Got: ${OUT}"
	    sed -i "s/^${BMARK},0,0,0,0,0$/${OUT}/" "$NFILE"
	    
	else
	    echo "Can't re-run $BMARK"
	fi
    done

    cd "$RDIR"
done

exit
