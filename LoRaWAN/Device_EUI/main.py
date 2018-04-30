# main.py -- put your code here!
from network import LoRa
import binascii
lora = LoRa(mode=LoRa.LORAWAN)

print("Getting LoRa EUI: ... \r\n")

print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))
