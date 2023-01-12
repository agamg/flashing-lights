from uqttsimple import MQTTClient
import network
from machine import Pin
from machine import I2C
from machine import PWM, Timer
import machine, neopixel
import time
from binascii import hexlify
import sys
import time
from time import sleep
import random
import math

n = 60
p = 21

np = neopixel.NeoPixel(machine.Pin(p), n)

#send IFTTT message
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("connecting to network:")
    wlan.active(True)
    wlan.connect('ME100-2.4G', '122Hesse') 
    while not wlan.isconnected():
        pass
          
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'sakeths819'
adafruitAioKey = 'aio_EnSN77DDV5jFLtKgYjPwSNfPLgUH'

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient("abcd", adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function su00b_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)
mqtt.connect()


#Calculate accleration in x direction, convert into values under 1
#IMU Setup
i2c = I2C(1,scl=Pin(22),sda=Pin(23),freq=400000)
for i in range(len(i2c.scan())):
    print(hex(i2c.scan()[i]))

def WHOAMI(i2caddr):
    whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
    print(hex(int.from_bytes(whoami,"little")))

def Xaccel(i2caddr):
    xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
    if xacc > 32767:
        xacc = xacc -65536
    print("X-acc: ")
    print("%4.2f" % (xacc/100))
    return xacc

def Yaccel(i2caddr):
    yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
    if yacc > 32767:
        yacc = yacc -65536

    print("Y-acc: ")
    print("%4.2f" % (yacc/10000))
    return yacc/1000

buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.1)

counter = 0

def demo(np, num, speed):
    n = np.n

    if (num == 1):
    # cycle
        
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            np[i % n] = (255, 255, 255)
            np.write()
            time.sleep_ms(25)

    if num == 2:
    # bounce
        for i in range(1 * n):
            for j in range(n):
                
                np[j] = (0, 0, 128)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 0)
            else:
                np[n - 1 - (i % n)] = (0, 0, 0)
            np.write()
            
            time.sleep_ms(60)

    if num == 3:
    # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                np[j] = (val, 0, 0)
            np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

while (1):
    WHOAMI(i2c.scan()[i])
    print(counter)

    counter = counter + 1
    
    livespeed = abs(int(Yaccel(i2c.scan()[i])))
    print(livespeed)

    if livespeed < 6:
        print(livespeed)
        demo(np,2,livespeed)
    else:
        time.sleep(1)
        demo(np,1,livespeed)
        #code to send data into the IQTTT, only send values above speed of 10. the IF statement is written inside the IQTTT, just need to send in values
        feedName = "sakeths819/feeds/ProjectSpeedFeed"
        testMessage = "75" #take the value of acceleration and put it into this value
        mqtt.publish(feedName,testMessage) #publish data into the service
        mqtt.subscribe(feedName)
        print("msg sent")
           
        
    

    

    

        