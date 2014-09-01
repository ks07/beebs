#!/bin/bash

# Set up ts
TS_MAXCONN=50 TS_SOCKET=/tmp/ts_execute tsp

RUN_DIRS=$(find . -maxdepth 1 -type d -name 'run-*')

for rd in $RUN_DIRS; do
 (
  cd $rd && TS_SOCKET=/tmp/ts_execute tsp -L "$rd" bash -c ../execute-pt2-alt.sh
 )
done
