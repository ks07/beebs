#!/bin/bash

RDIR=$(pwd -P)
NRGD=$(find . -name 'energy.csv*' -size +0 -printf '%h\n' | grep './run..*')
TO_FND=0

for d in $NRGD; do
    cd "$d" &&
    # Looks for tests in an energy.csv that have timed out, and attempts to re-run them.
    TMOUT=$(grep -x '.*,0,0,0,0,0' energy.csv* | sed 's/,0,0,0,0,0//')

    if [ -n "$TMOUT" ]; then
	(( TO_FND++ ))
	echo "TIMEOUTS IN: $d"
    fi

    cd "$RDIR"
done

if [[ "$TO_FND" -eq 0 ]]; then
    echo "NO TIMEOUTS FOUND"
fi

exit
