#!/bin/sh

# BEEBS Top Level Run script for AVR
# Copyright (C) 2014 Embecosm Limited

# Contributor Simon Cook <simon.cook@embecosm.com>
# Contributor Pierre Langlois <pierre.langlois@embecosm.com>

# This file is part of BEEBS

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# The arguments have the following meaning.

# Invocation Syntax

#     run.sh [--target-board <board>]

# --target-board <board>

CURDIR=$(dirname $0)
export DEJAGNU=$CURDIR/site.exp

export TARGET_TRIPLET=avr-unknown-none
export TARGET_ALIAS=avr

export AVR_MCU="atmega128"
export AVR_CFLAGS_EXTRA=""
export AVR_HEAP_END="0x800fff"
export AVR_LDFLAGS_EXTRA=""
export AVR_LDSCRIPT=""
export AVR_NETPORT="51000"
export AVR_STACK_SIZE="2048"
export AVR_TEXT_SIZE="131072"

TARGET_BOARD=avr-gdbserver

opt=$1
case ${opt} in
  --target-board)
    shift
    TARGET_BOARD=$1
    ;;
  *)
    ;;
esac

runtest --target_board=${TARGET_BOARD} \
  --tool=gcc --directory=gcc.beebs \
  --srcdir=$CURDIR execute.exp=gcc.beebs/*.c
