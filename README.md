# Temporary Development Branch

This branch holds the temporary state of the BEEBS repository for gathering
some data for training MAGEEC whilst BEEBSv2 is in development. This branch
should *not* be considered stable. Please use the beebsv2 branch in the
[mageec/beebs](https://github.com/mageec/beebs) repository instead.

Note in particular that for avr-rotate to work the listfile should be
modified and copied form listfile-orig.

# BEEBS: Open Benchmarks for Energy Measurements on Embedded Platforms

This repository contains the Bristol Energy Efficiency Benchmark Suite
(BEEBS).These benchmarks are designed to test the performance of deeply
embedded systems, particularly with regard to energy consumed. As such they
assume the presence of no OS and in particular no output stream.



For the paper describing the benchmarks and reasoning behind the choice of
benchmarks see http://arxiv.org/abs/1308.5174.

For an example of their use, see http://arxiv.org/abs/1303.6485.

## Compiling

The strength of the benchmark suite is the ability to run on embedded devices,
however the suite can also be compiled to be executed natively:

    $ ./configure
    $ make

This will create a benchmark in each directory in ./src. However, the
benchmark suite can be cross compiled for a number of architectures and
development boards. Each target needs the prerequisite tools installed:

 * STM32F0DISCOVERY
 * STM32VLDISCOVERY
 * Breadboarded ATMEGA328P (with USB to serial programmer)
 * Breadboarded PIC32MX250F128B (with PICKIT2 as a programmer)
 * SAM4L Xplained
 * XMEGA-A3BU Xplained Pro
 * MSP-EXP439F5529LP LaunchPad

Compiling for one these boards will produce executables for that board, which
toggle a specific pin at the beginning and end of the benchmark. This allows
them to be easily hooked up to other tools for time and energy measurements.

## Using the tests

All tests provide the functions initialize\_trigger (), start\_trigger () and
stop\_trigger () to control measurement of the test execution (performance,
energy consumed etc). The implementation of these functions should be provided
in platformcode.c.

The number of times each test is run is controlled by the constant
REPEAT_FACTOR set in the file platformcode.h. This should be edited as
required.

An example script to run all the tests is provided in run-all.sh. This script
was written to test the models compiled for the Atmel ATmega128 and running on
a remote target controlled by GDB. It should be modified as required for other
platforms.

## Versions of the tests

Different versions of the tests carry tags, to allow groups to agree on a
precise version used.

release-0.1: This version of BEEBS is described in Pallister, J., Hollis, S.,
& Bennett, J. (2013). BEEBS: Open Benchmarks for Energy Measurements on
Embedded Platforms. Available: http://arxiv.org/abs/1308.5174.

This is also the version used in Pallister, J., Hollis, S., & Bennett J.
(2013). "Identifying Compiler Options to Minimise Energy Consumption for
Embedded Platforms". Available http://arxiv.org/abs/1303.6485.



## Origin of the tests

All of these benchmarks are derived from other benchmark suites:

 * MiBench
 * WCET set of benchmarks
 * DSPstone

All are freely available for use, but some lack specific license
provisions. For the avoidance of doubt, the versions provided here are
explicitly licensed under the GNU General Public License version 3.


## Misc Notes

If build-aux/config.sub is regenerated, the following command needs to be run
to ensure pic32 is recognised as a valid tools prefix.

    sed -i 's/powerpcle \\/powerpcle \\\n    | pic32 \\/' $SCR_DIR/build-aux/config.sub
