#!/bin/sh

# BEEBS Top Level Run script
# Copyright (C) 2014 Embecosm Limited

# Contributor Simon Cook <simon.cook@embecosm.com>

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

CURDIR=$(dirname $0)
export DEJAGNU=$CURDIR/site.exp
runtest --tool=gcc --directory=gcc.beebs --srcdir=$CURDIR execute.exp=gcc.beebs/*.c
