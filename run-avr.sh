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
# --mcu <mcu>
# --cflags-extra <flags>
# --heap-end <val>
# --ldflags-extra <flags>
# --ldscript <scriptfile>
# --netport <port>
# --stack-size <val>
# --text-size <val>
# --avrdude <program>
# --avrdude-flags <val>
# --energytool-serial <val>
# --energytool-pin <val>
# --energytool-point <val>
# --trigger-file <file>
# --repeat-factor <val>
# --energy-data <file>

CURDIR=$(dirname $0)
export DEJAGNU=$CURDIR/site.exp

export TARGET_TRIPLET=avr-unknown-none
export TARGET_ALIAS=avr

# Default values for testing, overriden by their respective options.
AVR_MCU="atxmega256a3b"
AVR_CFLAGS_EXTRA=
AVR_HEAP_END=
AVR_LDFLAGS_EXTRA=
AVR_LDSCRIPT=
AVR_NETPORT=
AVR_STACK_SIZE=
AVR_TEXT_SIZE=

AVRDUDE="/opt/avrdude/bin/avrdude"
AVRDUDE_FLAGS="-cjtag3 -px256a3bu -C /opt/avrdude/etc/avrdude.conf -e"

TRIGGER_FILE="/tmp/trigger.c"

ENERGYTOOL_SERIAL="EE01"
ENERGYTOOL_PIN="PA0"
ENERGYTOOL_POINT=1

REPEAT_FACTOR=1

TARGET_BOARD=avr-avrdude

ENERGY_DATA="energy.json"

# Parse options
until
opt=$1
case ${opt} in
  --target-board)
    shift
    TARGET_BOARD=$1
    ;;

  --mcu)
    shift
    AVR_MCU="$1"
    ;;

  --cflags-extra)
    shift
    AVR_CFLAGS_EXTRA="$1"
    ;;

  --heap-end)
    shift
    AVR_HEAP_END="$1"
    ;;

  --ldflags-extra)
    shift
    AVR_LDFLAGS_EXTRA="$1"
    ;;

  --ldscript)
    shift
    AVR_LDSCRIPT="$1"
    ;;

  --netport)
    shift
    AVR_NETPORT="$1"
    ;;

  --stack-size)
    shift
    AVR_STACK_SIZE="$1"
    ;;

  --text-size)
    shift
    AVR_TEXT_SIZE="$1"
    ;;

  --avrdude)
    shift
    AVRDUDE="$1"
    ;;

  --avrdude-flags)
    shift
    AVRDUDE_FLAGS="$1"
    ;;

  --energytool-serial)
    shift
    ENERGYTOOL_SERIAL="$1"
    ;;

  --energytool-pin)
    shift
    ENERGYTOOL_PIN="$1"
    ;;

  --energytool-point)
    shift
    ENERGYTOOL_POINT="$1"
    ;;

  --trigger-file)
    shift
    TRIGGER_FILE="$1"
    ;;

  --repeat-factor)
    shift
    REPEAT_FACTOR="$1"
    ;;

  --energy-data)
    shift
    ENERGY_DATA="$1"
    ;;

  ?*)
    echo "Usage: ./run-avr.sh [--target-board <board>] <val>"
    echo "                    [--mcu <mcu>]"
    echo "                    [--cflags-extra <flags>]"
    echo "                    [--heap-end <val>]"
    echo "                    [--ldflags-extra <flags>]"
    echo "                    [--ldscript <scriptfile>]"
    echo "                    [--netport <port>]"
    echo "                    [--stack-size <val>]"
    echo "                    [--text-size <val>]"
    echo "                    [--avrdude <program>]"
    echo "                    [--avrdude-flags <val>]"
    echo "                    [--energytool-serial <val>]"
    echo "                    [--energytool-pin <val>]"
    echo "                    [--energytool-point <val>]"
    echo "                    [--trigger-file <file>]"
    echo "                    [--repeat-factor <val>]"
    echo "                    [--energy-data <file>]"

    exit 1
    ;;
  *)
    ;;
esac
[ "x${opt}" = "x" ]
do
    shift
done

export AVR_MCU
export AVR_CFLAGS_EXTRA
export AVR_HEAP_END
export AVR_LDFLAGS_EXTRA
export AVR_LDSCRIPT
export AVR_NETPORT
export AVR_STACK_SIZE
export AVR_TEXT_SIZE

export AVRDUDE
export AVRDUDE_FLAGS

export ENERGYTOOL_SERIAL
export ENERGYTOOL_PIN
export ENERGYTOOL_POINT

export TRIGGER_FILE

export REPEAT_FACTOR

export ENERGY_DATA

runtest --target_board=${TARGET_BOARD} \
  --tool=gcc --directory=gcc.beebs \
  --srcdir=$CURDIR execute.exp=gcc.beebs/*.c
