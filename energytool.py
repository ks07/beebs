#!/usr/bin/env python2

import pyenergy
import sys
from time import sleep

if len(sys.argv) is not 4:
  sys.stderr.write("nope\n")
  sys.exit(1)

em = pyenergy.EnergyMonitor(sys.argv[1])
em.connect()

em.enableMeasurementPoint(int(sys.argv[2]))
em.setTrigger(sys.argv[3])

while not em.measurementCompleted():
  sleep(0.1)

m = em.getMeasurement()

print "\"results\": {{ \"energy\": {}, \"time\": {}, \"avg_power\": {}, \"avg_current\": {}, \"avg_voltage\": {} }}".format(m.energy, m.time, m.avg_power, m.avg_current, m.avg_voltage)
