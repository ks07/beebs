#!/bin/sh
# Will convert and format hadamard matrices from neilsloane.com/hadamard/
cut -c 2- < "$1" | sed -e 's/+/   1/g' -e 's/-/  -1/g' | nl -w1 -v0 -s ''
