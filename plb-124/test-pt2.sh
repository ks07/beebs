#!/bin/bash
# Second level MAGEEC Test Script
# (This script is meant to be called by task spooler to run a job)
# Usage: "test-pt2.sh RUNNUMBER"

if [ "x$INMAGEEC" != "xTRUE" ]; then
	echo "This script should be run via the top level test.py" > /dev/stderr
	exit 1
fi

ROOT=$(dirname $0)

cd ${ROOT}/run-$1

date > output.log
export MAGEEC_EXECUTELIST=${ROOT}/run-$1/PASSES_TO_RUN

CFLAGS="-save-temps -fplugin=/usr/local/lib/libmageec_gcc.so -fplugin-arg-libmageec_gcc-dumppasses -O2" \
	${ROOT}/beebs/configure --disable-werror --host=avr --with-chip=atmega328p \
	--with-board=shrimp >> output.log 2>&1
if [ $? -gt 0 ]; then
	echo "Configure Failed" >> output.log 2>&1
	exit 1
fi

# We give the -k flag to make as we would expect some tests to fail to build
# at this stage, but want to build as many as possible.
# FIXME: Should this be removed for stable release, as this is really only
# for testing the framework and will almost always result in some failures?
make -k >> output.log 2>&1
gzip -9 output.log

# {{EXECUTION GOES HERE}}
