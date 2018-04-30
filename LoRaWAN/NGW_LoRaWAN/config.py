""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

'''
Added intop the code base GW Dewrived ID, this the ID derived
from the MAC of the wifi as shown below, I have printed this
out and given a more direct string below so  it can be easily
added to the GW portal for the TTN website
'''

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID_DERIVED = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

''' GW_ID ''' ''' 240ac4fffe025cac '''
'''TTN KEY from GW Registration'''
'''ttn-account-v2.yb777T2DgzvbRUmWNw9pHE6igdgMDHDtzUOo9ljJHDMl8lGxzNZ2Df1czoZf4tIvXu1LDU8yRFrP70Z83-2lzQ'''

GATEWAY_ID = '240AC4FFFE025CAC'

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'devolo-83d'
WIFI_PASS = 'BSWBPZOMKNCGBNDN'

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5

# for US915
# LORA_FREQUENCY = 903900000
# LORA_GW_DR = "SF7BW125" # DR_3
# LORA_NODE_DR = 3
