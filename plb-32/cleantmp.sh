#!/bin/sh
find /tmp/ -size 0 -name 'ts-out.*' -print0 | xargs -r0 rm
# Print any remaining.
find /tmp/ -name 'ts-out.*'
