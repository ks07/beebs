#!/bin/bash

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

#     run-avr-measurement.sh [--target-board <board>]

# --target-board <board>
# --avrdude <program>
# --avrdude-flags <val>
# --energytool-serial <val>
# --energytool-pin <val>
# --energytool-point <val>
# --energy-data <file>
# --timeout <val>

# Default values for testing, overriden by their respective options.
AVRDUDE="avrdude"
AVRDUDE_FLAGS="-carduino -patmega328p -P/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 -D -v"
ENERGYTOOL_SERIAL="MSP0"
ENERGYTOOL_PIN="PA0"
ENERGYTOOL_POINT=2

REPEAT_FACTOR=1

TARGET_BOARD=avr-avrdude

ENERGY_DATA="energy.csv"

TIMEOUT=120

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

  --energy-data)
    shift
    ENERGY_DATA="$1"
    ;;

  --timeout)
    shift
    TIMEOUT="$1"
    ;;

  ?*)
    echo "Usage: ./run-avr-measurement.sh [--target-board <board>]"
    echo "                                [--avrdude <program>]"
    echo "                                [--avrdude-flags <val>]"
    echo "                                [--energytool-serial <val>]"
    echo "                                [--energytool-pin <val>]"
    echo "                                [--energytool-point <val>]"
    echo "                                [--energy-data <file>]"
    echo "                                [--timeout <val>]"

    exit 1
    ;;
  *)
    ;;
esac
[ "x${opt}" = "x" ]
do
    shift
done

# Get us a target to execute on
# (I believe this means we need bash)
lockfile="$(dirname $0)/lockfile"
listfile="$(dirname $0)/listfile"
{
  flock -e 200

  if [ ! -s ${listfile} ]; then
    echo "No machine list available"
    exit 1
  fi

  # Get the top line
  line=`head -1 ${listfile}`

  # Remove the line from the file
  tail -n +2 ${listfile} > ${listfile}tmp
  mv ${listfile}tmp ${listfile}

} 200> ${lockfile}

AVRDUDE_DEVICE=`echo ${line} | cut -d ':' -f 1`
ENERGYTOOL_SERIAL=`echo ${line} | cut -d ':' -f 2`
ENERGYTOOL_PIN=`echo ${line} | cut -d ':' -f 3`
ENERGYTOOL_POINT=`echo ${line} | cut -d ':' -f 4`
AVRDUDE_FLAGS="-carduino -patmega328p -P${AVRDUDE_DEVICE} -D"

echo ${AVRDUDE_FLAGS}


export AVRDUDE
export AVRDUDE_FLAGS

export ENERGYTOOL_SERIAL
export ENERGYTOOL_PIN
export ENERGYTOOL_POINT

export ENERGY_DATA

export TIMEOUT

make RUNTESTFLAGS="--target_board=${TARGET_BOARD} measure.exp" check

# Put the board we took back in the pool
(
  flock -e 200
  echo ${line} >> ${listfile}
) 200> ${lockfile}
