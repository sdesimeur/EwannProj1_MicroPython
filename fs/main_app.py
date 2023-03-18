###########################################################################
# Setup code goes below, this is called once at the start of the program: #
###########################################################################
import time
import mywifi
from machine import Pin
import network


button = Pin(14,Pin.IN,Pin.PULL_UP)

#door2 = Pin(4,Pin.IN,None)
door1 = Pin(5,Pin.IN,None)

startNext = Pin(12,Pin.OUT)
relay1 = Pin(13,Pin.OUT)
relay2 = Pin(15,Pin.OUT)

def gpio_int(pin):
    if (pin==button):
        if (pin.value()==0):
            relay2.on()
            relay1.off()
    elif (pin==door1):
        if (pin.value()==0):
            relay1.on()
            relay2.off()
            startNext.off()
#    elif (pin==door2):
#        if (pin.value()==0):
#            relay2.off()



def main():
    relay1.on()
    relay2.on()
    startNext.on()
    button.irq(handler=gpio_int)
    door1.irq(handler=gpio_int)
    #door2.irq(handler=gpio_int)

    time.sleep(5.0)  # Delay for 1 second.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(mywifi.essid, mywifi.password)
    wlan.ifconfig()
    while True:
        time.sleep(1.0)  # Delay for 1 second.


