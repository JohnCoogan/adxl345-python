# ADXL345 Daemon to watch for activity 
#
# author:  John Coogan
# license: BSD, see LICENSE.txt included in this package
# 
# This script listens for changes in net G-Force
# Relies on the ADXL345 accelerometer.
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

from adxl345 import ADXL345
  
adxl345 = ADXL345()
    
axes = adxl345.getAxes(True)
print "ADXL345 on address 0x%x:" % (adxl345.address)
print "   x = %.3fG" % ( axes['x'] )
print "   y = %.3fG" % ( axes['y'] )
print "   z = %.3fG" % ( axes['z'] )

oldaxes = dict(axes)

while True:
    axes = adxl345.getAxes(True)
    deltas = {k:abs(v - oldaxes[k]) for k,v in axes.items()}
    total_force = sum(deltas.values())
    if total_force > 0.1:
        print "Felt a bump in the night"
    oldaxes = dict(axes)
