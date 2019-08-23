#!/usr/bin/python
import time
from TSL2581 import TSL2581

try:
    Light=TSL2581(0X39, debug=False)

    id=Light.Read_ID() & 0xf0
    print('ID = %#x'%id)
    Light.Init_TSL2581()
    
    while True:
      lux  =  Light.calculate_Lux()
      print"lux = ", lux
      time.sleep(1)

except:
    # GPIO.cleanup()
    print "\nProgram end"
    exit()