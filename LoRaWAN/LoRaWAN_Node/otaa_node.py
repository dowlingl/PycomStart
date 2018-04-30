""" OTAA Node example compatible with the LoPy Nano Gateway """

import pycom

from network import LoRa
import socket
import binascii
import struct
import time
import config

from machine import Pin
from onewire import DS18X20
from onewire import OneWire

'''
DEFINED CONSTANTS USED FOR HOUSE KEEPING
VERSION NUMBER WILL [ MM.NN ]
'''

'''  MM == Major Major Number '''
mm = 00
''' NN == Minor Minor Number'''
nn = 14

''' NODE WIFI MAC BASED''' '''240AC4FFFE0238E0'''
'''DEVICE EUI, LoRA MAC BASED''' ''' 70B3D54990410FDD '''
''' House Keeping'''
verStr = str(mm) + "." + str(nn)

pycom.heartbeat(False)
#pycom.heartbeat(True)
pycom.rgbled(0x000000)

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTA authentication params
''' OLD CODE ; dev_eui = binascii.unhexlify('AABBCCDDEEFF7778') '''
dev_eui = binascii.unhexlify('70B3D54990410FDD') # Retreived from LoRa MAC

# app_eui = binascii.unhexlify('446f77536f667401')

app_eui = binascii.unhexlify('70B3D57ED000C010')

#app_key = binascii.unhexlify('36AB7625FE770B6881683B495300FFD6')
''' From TTN ''' ''' 8EC87A2F9273CCDA1E0C1B52E4C87B94 '''
app_key = binascii.unhexlify('8EC87A2F9273CCDA1E0C1B52E4C87B94')

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)
print("Starting a LoraWAN Node .... VER: %s " % verStr )
connectionAttempts = 1
# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print("Not joined yet... #%d \r\n" % connectionAttempts )
    connectionAttempts+=1
'''
DEBUGING ONLY----
    print("APP KEY USED: %s \r\n" % app_key )
    print("APP EUI USED: %s \r\n" % app_eui )
    print("DEV EUI USED: %s \r\n" % dev_eui )
'''

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket blocking
s.setblocking(False)

#DS18B20 data line connected to pin P23
ow = OneWire(Pin('P23'))
temp = DS18X20(ow)

time.sleep(5.0)
print("Connected .... ")
pycom.rgbled(0x007f00)           # turn on the RGB LED in green colour

test_str = "::This is Test"
PRINTING__DEBUG = True

'''
for i in range (200):
    pkt = b'PKT #' + bytes([i]) + test_str
    pycom.rgbled(0xff0000)           # turn on the RGB LED in green colour
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(0.2)
    pycom.rgbled(0x000000)           # turn Off LED
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
'''

p_out = Pin('P9', mode=Pin.OUT)


while True:
    p_out.value(1)
    temp.start_conversion()
    time.sleep(1)
    ''' obtain the temperature string '''
    temp_t = temp.read_temp_async()
    ''' Convert the float plus string into one string '''
    t_str ="T = " + "%8.4f" % temp_t

    if PRINTING__DEBUG == True:
        ''' Print it oput to prove the string looks OK '''
        print("This the the temperature %s " % t_str )
        ''' Check length is constant '''
        strLen = len(t_str)
        print("This the length %d " % strLen )

    pkt = b'PKT #' + "::" + t_str
    if PRINTING__DEBUG == True:
        print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        if PRINTING__DEBUG == True:
            print('Received: {}, on port: {}'.format(rx, port))
    p_out.value(0)
    time.sleep(6)
