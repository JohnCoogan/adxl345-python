# ADXL345 Daemon to watch for activity 
#
# author:  John Coogan
# license: BSD, see LICENSE.txt included in this package
# 
# This script listens for changes in net G-Force
# Relies on the ADXL345 accelerometer.
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

from adxl345 import ADXL345
import time
import os
import sys

try:  
   os.environ["GSHEETS"]
except KeyError: 
   print "Please set the environment variable GSHEETS"
   sys.exit(1)

adxl345 = ADXL345()

axes = adxl345.getAxes(True)
print "ADXL345 on address 0x%x:" % (adxl345.address)
print "   x = %.3fG" % ( axes['x'] )
print "   y = %.3fG" % ( axes['y'] )
print "   z = %.3fG" % ( axes['z'] )

oldaxes = dict(axes)

start_time = time.time()
minute_force = 0
minute_bumps = 0


def log_results(minute_force, minute_bumps):
    print "Total Force this minute: %.3fG" % minute_force
    print "Total Bumps this minute: %.3fG" % minute_bumps
    return


while True:
    diff_time = time.time() - start_time
    if diff_time >= 60.0:
        start_time = time.time()
        log_results(minute_force, minute_bumps)
        minute_force = 0
        minute_bumps = 0
    axes = adxl345.getAxes(True)
    deltas = {k:abs(v - oldaxes[k]) for k,v in axes.items()}
    total_force = sum(deltas.values())
    minute_force += total_force
    if total_force > 0.25:
        minute_bumps += 1
    oldaxes = dict(axes)
