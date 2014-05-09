/* -*- mode: C; c-file-style: "gnu-mode" -*- */
/* BEEBS Dummy Platform Code

   Copyright (C) 2014 Embecosm Limited and University of Bristol

   Contributor: Simon Cook <simon.cook@embecosm.com>

   This file is part of the Bristol/Embecosm Embedded Energy Benchmark Suite.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>. */

#ifndef __PLATFORMCODE_H__
#define __PLATFORMCODE_H__

#ifndef REPEAT_FACTOR
#define REPEAT_FACTOR   (4096)
#endif

void initialise_trigger() {}
void stop_trigger() {}
void start_trigger() {}

#endif /* __PLATFORMCODE_H__ */
