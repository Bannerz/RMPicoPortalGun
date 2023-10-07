# IMPORTS
import math
import time
from machine import I2C, Pin, RTC
from ht16k33segment import HT16K33Segment

# CONSTANTS
DELAY = 0.01
PAUSE = 3

btn = Pin(12, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(14, Pin.IN, Pin.PULL_UP)
step_pin = Pin(15, Pin.IN, Pin.PULL_UP)

previous_value = True
button_down = False

dimensionArray = [0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D, 0x76, 0x30, 0x1E,
                  0x75, 0x38, 0x55, 0x37, 0x3f, 0x73, 0x67, 0x31, 0x6D, 0x78, 0x3E,
                  0x1C, 0x1D, 0x64, 0x6E, 0x5B, 0x00]


dimNumArray = []


#leds
#front leds
frntLed1 = machine.Pin(2, machine.Pin.OUT)
frntLed2 = machine.Pin(3, machine.Pin.OUT)
frntLed3 = machine.Pin(4, machine.Pin.OUT)

#top leds
topLed1 = machine.Pin(9, machine.Pin.OUT)
topLed2 = machine.Pin(22, machine.Pin.OUT)

#turn led on
frntLed1.high() #middle
frntLed2.high() #sides
frntLed3.high()
topLed1.high()
topLed2.high()
dimNum = 137 #dimension number
dimCounter = 3 #dimension letter 1=a 2=b 3=c etc

while True:
    
    if dimNum > 999:
        dimNum = 001
        dimCounter += 1
        
    if dimNum < 001:
        dimNum = 999
        dimCounter -= 1
        
    if dimCounter > 26:
        dimCounter = 1
    
    if dimCounter < 1:
        dimCounter = 26
        

    if previous_value != step_pin.value():
        if step_pin.value() == False:
            if direction_pin.value() == False:
                dimNum -= 1
                dimNum=dimNum
                print(dimNum)
                print(dimCounter)
                
                
            else:
                dimNum += 1
                print(dimNum)
                print(dimCounter)
        previous_value = step_pin.value()
        
    
 
                    
            
    withZero = "{:03d}".format(dimNum)
    
    combinedNum = int(str(dimCounter) + str(withZero)) #total dimension number
    fixedDimNum = int(str(1) + str(withZero)) #total dimension number        
    dimNumArray = [int(x) for x in str(combinedNum)]
    fixedDimNumArray = [int(x) for x in str(fixedDimNum)]
        
    # START
    if __name__ == '__main__':
        
    
        i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # PicoLipo i2c pins

        display = HT16K33Segment(i2c)
        display.set_brightness(20)
        
        dimNumUpdate = fixedDimNumArray[1]
        dimNumUpdate1 = fixedDimNumArray[2]
        dimNumUpdate2 = fixedDimNumArray[3]

        # Write dimension to the display using the glyphs and numbers
        display.set_glyph(dimensionArray[dimCounter], 0).set_number(dimNumUpdate, 1)
        display.set_number(dimNumUpdate1, 2).set_number(dimNumUpdate2, 3)
        display.draw()
    
    
    if btn.value() == False and not button_down:
        frntLed1.low()
        frntLed2.low()
        frntLed3.low()
        time.sleep(0.5)
        frntLed2.high()
        frntLed3.high()
        time.sleep(0.2)
        frntLed1.high()
        
        topLed1.low()
        time.sleep(0.1)
        topLed2.high()
        time.sleep(0.1)
        topLed1.high()
        time.sleep(0.1)
        topLed2.low()
        time.sleep(0.1)
        topLed1.low()
        time.sleep(0.1)
        topLed2.high()
        time.sleep(0.1)
        topLed1.high()
        time.sleep(0.1)
        topLed2.low()
        time.sleep(0.1)
        topLed2.high()
        time.sleep(0.1)
        topLed1.low()
        time.sleep(0.1)
        topLed2.high()
        time.sleep(0.1)
        topLed1.high()
        time.sleep(0.1)
        topLed2.low()
        time.sleep(0.1)
        topLed1.low()
        time.sleep(0.1)
        topLed2.high()
        time.sleep(0.1)
        topLed1.high()
        time.sleep(0.1)
        topLed2.low()
        time.sleep(0.1)
        topLed2.high()
        button_down = True
    if btn.value() == True and button_down:
        button_down = False
    
        
        
