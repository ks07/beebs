#!/bin/bash

# Repeat the tests 3 times
for i in {1..3}; do
    ../beebs/run-avr-rotate.sh > execute.log 2>&1
    mv -n energy.csv "energy.csv.$i"
done
