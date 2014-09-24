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
from datetime import datetime
import os
import sys
import sheetsync
import multiprocessing

try:  
    pw = os.environ["GSHEETS"]
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
results = {'force': 0, 'bumps': 0}
target = sheetsync.Sheet(username="coogan.johna@gmail.com", password=pw, document_name="SleepLog")


def log_results(result_log):
    target.inject({datetime.now():result_log})
    print "Total Force this minute: %.3fG" % result_log['force']
    print "Total Bumps this minute: %i" % result_log['bumps']
    return


while True:
    diff_time = time.time() - start_time
    if diff_time >= 60.0:
        print datetime.now()
        start_time = time.time()
        result_log = dict(results)
        multiprocessing.Process(target=log_results, args=(result_log,)).start()
        log_results(result_log)
        results = {'force': 0, 'bumps': 0}
    axes = adxl345.getAxes(True)
    deltas = {k:abs(v - oldaxes[k]) for k,v in axes.items()}
    total_force = sum(deltas.values())
    results['force'] += total_force
    if total_force > 0.25:
        results['bumps'] += 1
    oldaxes = dict(axes)
