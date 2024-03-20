#Updated Circuitpython code for Raspberry Pi Pico (RP2040)
#to make the Portal Gun project REALLY come to life

#Version: 2.3
#Author: Alex Banfield
#Copyright: 2024

#imports
import board
import digitalio
import time
import array
import math
import audiocore
import audiobusio
import audiomp3
import rotaryio
from adafruit_ht16k33.segments import Seg7x4
import busio
import random


#timings for top LEDs
BLINK_LIST = [
    {
        "ON": random.uniform(0.05, 0.2),
        "OFF": random.uniform(0.05, 0.2),
        "PREV_TIME": -1,
        "PIN": board.GP6,
    },
    {
        "ON": random.uniform(0.05, 0.2),
        "OFF": random.uniform(0.05, 0.2),
        "PREV_TIME": -1,
        "PIN": board.GP22,
    }
]

#timings for front LEDs
FRONT_LIST = [
    {
        "ON": random.uniform(0.05, 0.2),
        "OFF": random.uniform(0.05, 0.2),
        "PREV_TIME": -1,
        "PIN": board.GP2,
    },
    {
        "ON": random.uniform(0.05, 0.2),
        "OFF": random.uniform(0.05, 0.2),
        "PREV_TIME": -1,
        "PIN": board.GP3,
    },
    {
        "ON": random.uniform(0.05, 0.2),
        "OFF": random.uniform(0.05, 0.2),
        "PREV_TIME": -1,
        "PIN": board.GP4,
    }
]

#initialise both lists of LEDs
for led in BLINK_LIST:
    led["PIN"] = digitalio.DigitalInOut(led["PIN"])
    led["PIN"].direction = digitalio.Direction.OUTPUT
    
for led in FRONT_LIST:
    led["PIN"] = digitalio.DigitalInOut(led["PIN"])
    led["PIN"].direction = digitalio.Direction.OUTPUT

#initialise display on i2c
i2c = busio.I2C(board.GP17, board.GP16)
display = Seg7x4(i2c)

#initialise i2s audio
audio = audiobusio.I2SOut(board.GP7, board.GP8, board.GP9)
#get mp3 sound (must be in root dir on pico)
mp3 = audiomp3.MP3Decoder(open("sound1.mp3", "rb"))
#initialise encoder
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
encoder.position = 137  #set the initial position to 137
last_position = encoder.position
letter_index = 2  #index of the alphabet letter 'C'

#update display with initial values
display[0] = 'C'
display[1] = '1'
display[2] = '3'
display[3] = '7'

#initialise button
button = digitalio.DigitalInOut(board.GP13)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

button_state = None

#main loop
while True:
    #get time
    now = time.monotonic()
    #button logic    
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        #play the sound
        audio.play(mp3)
        while audio.playing:
            #while playing the sound do the animations
            now = time.monotonic()
            for led in BLINK_LIST:
                if led["PIN"].value is False:
                    if now >= led["PREV_TIME"] + led["OFF"]:
                        led["PREV_TIME"] = now
                        led["PIN"].value = True
                if led["PIN"].value is True:
                    if now >= led["PREV_TIME"] + led["ON"]:
                        led["PREV_TIME"] = now
                        led["PIN"].value = False
            for led in FRONT_LIST:
                if led["PIN"].value is False:
                    if now >= led["PREV_TIME"] + led["OFF"]:
                        led["PREV_TIME"] = now
                        led["PIN"].value = True
                if led["PIN"].value is True:
                    if now >= led["PREV_TIME"] + led["ON"]:
                        led["PREV_TIME"] = now
                        led["PIN"].value = False
        #set the front leds to off when sound ends
        for led in FRONT_LIST:
            led["PIN"].value = False
        button_state = None
    #do the top led animation
    for led in BLINK_LIST:
        if led["PIN"].value is False:
            if now >= led["PREV_TIME"] + led["OFF"]:
                led["PREV_TIME"] = now
                led["PIN"].value = True
        if led["PIN"].value is True:
            if now >= led["PREV_TIME"] + led["ON"]:
                led["PREV_TIME"] = now
                led["PIN"].value = False
 
     #read the current position of the rotary encoder
    position = encoder.position
    
    #check if the position has changed since the last iteration
    if position != last_position:
        #limit position to 0-999 range
        position %= 1000
        
        #check for rollover from 000 to 999
        if last_position == 0 and position == 999:
            #decrement letter index
            letter_index = (letter_index - 1) % 26
            
            #update the displayed characters on the 7-segment display
            letter = chr(ord('A') + letter_index)
            display[0] = letter
            display[1] = str(position // 100)
            display[2] = str((position // 10) % 10)
            display[3] = str(position % 10)
            
            #update the last position
            last_position = position
            continue  #skip further processing for this iteration
        
        #check for rollover from 999 to 000
        elif last_position == 999 and position == 0:
            #increment letter index
            letter_index = (letter_index + 1) % 26
            
            #update the displayed characters on the 7-segment display
            letter = chr(ord('A') + letter_index)
            display[0] = letter
            display[1] = str(position // 100)
            display[2] = str((position // 10) % 10)
            display[3] = str(position % 10)
            
            #update the last position
            last_position = position
            continue  # Skip further processing for this iteration
        
        #update the displayed characters on the 7-segment display
        letter = chr(ord('A') + letter_index)
        display[0] = letter
        display[1] = str(position // 100)
        display[2] = str((position // 10) % 10)
        display[3] = str(position % 10)
        
        #update the last position
        last_position = position