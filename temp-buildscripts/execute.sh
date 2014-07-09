#!/bin/bash

# Set up ts
TS_MAXCONN=50 TS_SOCKET=/tmp/ts_execute ts

for i in {1..32768}; do
 (
  cd run-$i && TS_SOCKET=/tmp/ts_execute ts bash ../execute-pt2.sh
 )
done
