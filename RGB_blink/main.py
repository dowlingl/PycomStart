# main.py -- put your code here!
import pycom
import time

print("Stopping HeartBeat !!! \r\n")
pycom.heartbeat(False)


while True:
    print( "LED: --> RED     \r\n" )
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)

    print( "LED: --> GREEN   \r\n" )
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)

    print( "LED: --> BLUE    \r\n" )
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)
