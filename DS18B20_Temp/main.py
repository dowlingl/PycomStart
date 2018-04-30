import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

nn = 00
mm = 07
#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P23'))
temp = DS18X20(ow)
verStr = str(nn)+"."+str(mm)

print( "Starting One Wire Test ... VER: %s" % verStr )

while True:
    temp.start_conversion()
    time.sleep(1)
    ''' obtain the temperature string '''
    temp_t = temp.read_temp_async()
    ''' Convert the float plus string into one string '''
    t_str ="T = " + "%8.4f" % temp_t
    ''' Print it oput to prove the string looks OK '''
    print("This the the temperature %s " % t_str )
    ''' Check length is constant '''
    strLen = len(t_str)
    print("This the length %d " % strLen )
    time.sleep(1)
