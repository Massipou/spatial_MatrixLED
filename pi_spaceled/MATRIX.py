#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import socket
import math

NET_AUDIO = True

# LED strip configuration:
LED_COUNT      = 600      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 12      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

DOWN = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

ORANGE = Color(255, 60, 0)
YELLOW = Color(255, 255, 0)

ACIDBLUE = Color(240,248,255)
REDPURP = Color(180, 0, 25)
TURQOISE = Color(0, 255, 125)
REBECCAPURPLE = Color(102, 51, 153)
DARKVIOLET = Color(125, 0, 125)
BLUEPURP = Color(10, 0, 255)
REDDORANG = Color(125, 30, 30)
MAGICRED = Color(255, 0, 20)

instruction = ""
start = True

def connect():
    global s
    global clientsocket, clientaddress
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.5.1', 8088))
    print (socket.gethostname())
    s.listen(1)
    clientsocket, clientaddress = s.accept()
    print(f"Connection from {clientaddress} has been established.") 

def reconnect():
    global clientsocket, clientaddress
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.1.243', 8088))
    print (socket.gethostname())
    s.listen(1)
    clientsocket, clientaddress = s.accept()
    print(f"Connection from {clientaddress} has been established.") 

def pat_control():
    global instruction
    global start
    if pixel_map.instruction == "skip": start = False

connect()

class pixel_map:
    def init():
        pixel_map.zoom = 1
        pixel_map.gap = []

        pixel_map.rmap = [0] * (LED_COUNT + 1)
        pixel_map.gmap = [0] * (LED_COUNT + 1)
        pixel_map.bmap = [0] * (LED_COUNT + 1)

        pixel_map.effect = 0
        pixel_map.effectoption = 1
        pixel_map.gap_effect = False
        pixel_map.effect_list = []
        pixel_map.gap_effect_div = 5
        pixel_map.gap_effect_pos = 1
        pixel_map.time_wait = 1 #second
        pixel_map.last_time = time.perf_counter()
        pixel_map.last_elapsed_time = 0
        pixel_map.instruction = ""
        pixel_map.pixel_number = LED_COUNT

        pixel_map.acid = True
        pixel_map.acidposlist = [0]
        pixel_map.acidlen = 0

        i = 1
        loop = True
        #for i in range (1, pixel_map.pixel_number, 1):
        while loop == True:
            nop = int(round(math.sin(i/3) * 4 + 5)) #NUMBER OF PIXELS FOR EACH PIXELS
            pixelpos = pixel_map.acidposlist[i - 1] + nop
            if pixelpos <= pixel_map.pixel_number:
                pixel_map.acidposlist.append(pixelpos)
                #print (pixel_map.acidposlist[i])
            else:
                loop = False
                pixel_map.acidlen = len(pixel_map.acidposlist)
                print (pixel_map.acidlen)
            i = i + 1

        if pixel_map.acid: pixel_map.pixel_number = pixel_map.acidlen

pixel_map.init()

def pixel_mapper(strip, index, r, g, b):

    lol = 1.5
    acid = pixel_map.acid

    acidlist = pixel_map.acidposlist
    if not acid: pixel_map.pixel_number = int(round(LED_COUNT/pixel_map.zoom))
    else: pixel_map.pixel_number = pixel_map.acidlen
    pixels_number = pixel_map.pixel_number

    pixel_map.gap = []
    effect = pixel_map.effect

    if effect >= 1 and effect <= 7:
        if r == 0 and g == 0 and b == 0:
            #print("{} {} {}" .format(r, g, b))
            if pixel_map.rmap[index] != 0 or pixel_map.gmap[index] != 0 or pixel_map.bmap[index] != 0:
                #print (pixel_map.effectoption)
                effect_option = float(pixel_map.effectoption)
                if effect_option != 0:
                    if effect == 1:
                        r = int(round(pixel_map.rmap[index]/effect_option))
                        g = int(round(pixel_map.gmap[index]/effect_option))
                        b = int(round(pixel_map.bmap[index]/effect_option))
                    elif effect == 2:
                        r = int(round(pixel_map.rmap[index]/(effect_option*lol)))
                        g = int(round(pixel_map.gmap[index]/(effect_option*lol)))
                        b = int(round(pixel_map.bmap[index]/effect_option))
                    elif effect == 3:
                        r = int(round(pixel_map.rmap[index]/effect_option))
                        g = int(round(pixel_map.gmap[index]/(effect_option*lol)))
                        b = int(round(pixel_map.bmap[index]/(effect_option*lol)))
                    elif effect == 4:
                        r = int(round(pixel_map.rmap[index]/(effect_option*lol)))
                        g = int(round(pixel_map.gmap[index]/(effect_option)))
                        b = int(round(pixel_map.bmap[index]/(effect_option*lol)))
                    elif effect == 5:
                        r = int(round(pixel_map.rmap[index]/(effect_option*lol)))
                        g = int(round(pixel_map.gmap[index]/effect_option))
                        b = int(round(pixel_map.bmap[index]/effect_option))
                    elif effect == 6:
                        r = int(round(pixel_map.rmap[index]/effect_option))
                        g = int(round(pixel_map.gmap[index]/(effect_option*lol)))
                        b = int(round(pixel_map.bmap[index]/effect_option))
                    elif effect == 7:
                        r = int(round(pixel_map.rmap[index]/effect_option))
                        g = int(round(pixel_map.gmap[index]/effect_option))
                        b = int(round(pixel_map.bmap[index]/(effect_option*lol)))


    pixel_map.rmap[index] = r
    pixel_map.gmap[index] = g
    pixel_map.bmap[index] = b

    if acid == True:
        ci = index - 1
        #print(ci)
        #print(pixel_map.pixel_number)
        if ci > 0 and ci < len(acidlist):
            nopbrut = acidlist[ci]
            if ci == 0: starter = 1
            else: starter = acidlist[ci - 1]
            if nopbrut <= LED_COUNT:
                #print ("{} {}" .format(starter, nopbrut))
                for i in range (starter, nopbrut, 1):
                    strip.setPixelColor(i, Color(r, g, b))

    #print("{} {} {}".format(r, g, b))

    else:

        if pixel_map.zoom != 0: zoom = pixel_map.zoom

        if zoom == 1:
            strip.setPixelColor(index, Color(r, g, b))
        else:
            for i in range (index*zoom, (index+1)*zoom, 1):
                strip.setPixelColor(i, Color(r, g, b))

# get_data return brut datas and an array of the datas from client
def get_datas():
    dataFromClient = clientsocket.recv(4096)
    return dataFromClient, dataFromClient.decode().split()

def template(number):

    if number == 1:
        pixel_map.acid = True
        pixel_map.effect = 6
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 1

    elif number == 2:
        pixel_map.acid = True
        pixel_map.effect = 6
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 1

    elif number == 3:
        pixel_map.acid = False
        pixel_map.effect = 6
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 5

    elif number == 4:
        pixel_map.acid = False
        pixel_map.effect = 6
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 5

    elif number == 5:
        pixel_map.acid = False
        pixel_map.effect = 6
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 10

    elif number == 6:
        pixel_map.acid = True
        pixel_map.effect = 7
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 1

    elif number == 7:
        pixel_map.acid = True
        pixel_map.effect = 7
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 1

    elif number == 8:
        pixel_map.acid = False
        pixel_map.effect = 7
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 5

    elif number == 9:
        pixel_map.acid = False
        pixel_map.effect = 7
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 5

    elif number == 10:
        pixel_map.acid = False
        pixel_map.effect = 7
        pixel_map.effectoption = 1.5
        pixel_map.zoom = 10

    elif number == 11:
        pixel_map.acid = False
        pixel_map.effect = 6
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 10

    elif number == 10:
        pixel_map.acid = False
        pixel_map.effect = 7
        pixel_map.effectoption = 1.1
        pixel_map.zoom = 10



# freq_to_color2 colors send by client and return it
def freq_to_color2():
    r, g, b = 0, 0, 0
    dataBrut, datas = get_datas()
    data = ""
    if len(datas) >= 5:
        #print(int(datas[4]))
        r, g, b, pixel_map.instruction = int(datas[0]), int(datas[1]), int(datas[2]), datas[3]
        if float(datas[4]) > 0 and pixel_map.instruction == "zoom" :
             pixel_map.zoom = int(datas[4])
             print (pixel_map.zoom)
             print ("lol")
        elif pixel_map.instruction == "acid":
            if pixel_map.acid == True: pixel_map.acid = False
            else : pixel_map.acid = True
            print(pixel_map.acid)
        elif pixel_map.instruction == "template":
            pixel_map.tempnumber = template(int(datas[4]))
        elif pixel_map.instruction != "skip":
            if int(pixel_map.instruction) >= 1:
                 pixel_map.effect = int(pixel_map.instruction)
                 pixel_map.effectoption = float(datas[4])
                 #print (pixel_map.effect)
                 #print ("lol")

    #if len(datas) >= 4: print("{}, {}, {}, {}, {}" .format(r,g,b,pixel_map.instruction,int(datas[4])))
    if not bool(dataBrut.decode()):
        print ("vide")
    #print ("{} {} {}".format(r, g, b))
    return (r, g, b)


def sound_react(strip,loop,color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    for i in range (loop):
        for j in range (strip.numPixels()):
            strip.setPixelColor(j+1, DOWN)
            color = freq_to_color(color1,color2,color3,color4,color5)
            strip.setPixelColor(j, color)
            strip.show()

def sound_react_div(strip, loop, div, funk=2, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    while start:
        for j in range (0,div,1):
            if funk == 1: color = freq_to_color(color1,color2,color3,color4,color5)
            else: color = freq_to_color2()
            for k in range (1,pixel_number,div):
                pixel_mapper(strip, k+j, color)
            strip.show()
            pat_control()

def sound_react_mov(strip, loop, invert=False, funk=2, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    rlist = [0] * (pixel_number)
    glist = [0] * (pixel_number)
    blist = [0] * (pixel_number)
    print (pixel_map.pixel_number)

    while start:
        if pixel_number != pixel_map.pixel_number:
            pixel_number = pixel_map.pixel_number
            rlist = [0] * (pixel_number)
            glist = [0] * (pixel_number)
            blist = [0] * (pixel_number)

        for j in range (pixel_number):
            if funk == 2:
                #rlist[j], glist[j], blist[j] = freq_to_color2()
                r, g, b = freq_to_color2()
                rlist[j] = r
                glist[j] = g
                blist[j] = b
                #print("{} {} {}".format(r, g, b))
            for k in range (pixel_number):
                if not invert: pixel_mapper(strip, k, rlist[j-k], glist[j-k], blist[j-k])
                else: pixel_mapper(strip, pixel_number-k, rlist[j-k], glist[j-k], blist[j-k])
            strip.show()
            pat_control()

def sound_react_mov_mirror(strip, loop, invert=False, funk=2, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    colorlist = [DOWN]*(pixel_number+1)
    middle = int(round(pixel_number/2))
    pixel_number = pixel_map.pixel_number
    while start:
        for j in range (pixel_number, 0, -1):
            if funk == 1: colorlist[j] = freq_to_color(color1,color2,color3,color4,color5)
            else: colorlist[j] = freq_to_color2()
            for k in range (middle+1):
                if not invert:
                    # strip.setPixelColor(k, colorlist[j-k-middle])
                    pixel_mapper(strip, k, colorlist[j-k-middle])
                    # strip.setPixelColor(strip.numPixels()-k, colorlist[j-k-middle])
                    pixel_mapper(strip, pixel_number-k, colorlist[j-k-middle])

                else: 
                    # strip.setPixelColor(middle + k, colorlist[j-k-middle])
                    pixel_mapper(strip, middle + k, colorlist[j-k-middle])
                    # strip.setPixelColor(middle - k, colorlist[j-k-middle])
                    pixel_mapper(strip, middle - k, colorlist[j-k-middle])
            middle = int(round(pixel_number/2))
            strip.show()
            pat_control()


def sound_react_mov_mirror_div(strip, loop, invert=False, funk=2, div=30, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    colorlist = [DOWN]*(pixel_number+1)
    true_middle = int(round(pixel_number/2))
    middle = int(round(div/2))
    div_number = int(round(pixel_number/div)*2)
    while start:
        for j in range (pixel_number):
            if funk == 1: colorlist[j] = freq_to_color(color1,color2,color3,color4,color5)
            else: colorlist[j] = freq_to_color2()
            for l in range (0, div_number, 1):
                diff = int(round(l*div))
                for k in range (0, middle+1):
                    if not invert:
                        pixel_mapper(strip, middle+k + diff, colorlist[j-k])
                        pixel_mapper(strip, middle-k + diff, colorlist[j-k])
                    else: 
                        pixel_mapper(strip, middle+diff + k, colorlist[j-k-middle])
                        pixel_mapper(strip, middle+diff - k, colorlist[j-k-true_middle])
            strip.show()
            pat_control()

def sound_react_mov_mirror_div2(strip, loop, invert=False, funk=2, div=30, mov=50, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    colorlist = [DOWN]*(pixel_number+1)
    true_middle = int(round(pixel_number/2))
    middle = int(round(div/2))
    div_number = int(round(pixel_number/div)*2)
    while start:
        for j in range (pixel_number):
            if funk == 1: colorlist[j] = freq_to_color(color1,color2,color3,color4,color5)
            else: colorlist[j] = freq_to_color2()
            for m in range (mov):
                for k in range (0, middle+1):
                    for l in range (0, div_number, 1):
                        diff = int(round(l*div))
                        for k in range (0, middle+1):
                            if not invert:
                                pixel_mapper(strip, middle+k+m + diff, colorlist[j-k])
                                pixel_mapper(strip, middle-k+m + diff, colorlist[j-k])
                            else: 
                                pixel_mapper(strip, middle+diff + k+m, colorlist[j-k-middle])
                                pixel_mapper(strip, middle+diff - k+m, colorlist[j-k-true_middle])
                    strip.show()
                    pat_control()


def sound_react_div_mov(strip, loop, div, funk=2, color1=RED, color2=ORANGE, color3=YELLOW, color4=GREEN, color5=BLUE, wait_ms=50):
    global start
    start = True
    pixel_number = pixel_map.pixel_number
    while start:
        for j in range (0,div,1):
            for l in range (0,div,1):
                if funk == 1: color = freq_to_color(color1,color2,color3,color4,color5)
                else: color = freq_to_color2()
                for k in range (1,pixel_number,div):
                    pixel_mapper(strip, k+j+l, color)
                strip.show()
                pat_control()

def colorWipe(strip, color, color2, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        if i%10 < 5:
            strip.setPixelColor(i, color2)
        strip.show()
        time.sleep(wait_ms/1000.0)


def colorSlide(strip, color, color2, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        if i%10 == 0:
            stripenumber = int(i/5)+5
        for j in range (stripenumber):
            if j%2 == 0:
                strip.setPixelColor(i-(j*5), color2)
            else:
                strip.setPixelColor(i-(j*5), color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def doubleColorSlide(strip, color, color2, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    numpixel = int(round(strip.numPixels()/2, 0))
    for i in range(numpixel):
        strip.setPixelColor(i, color)
        if i%10 == 0:
            stripenumber = int(i/5)+5
        for j in range (stripenumber):
            if j%2 == 0:
                strip.setPixelColor(i-(j*5), color2)
                strip.setPixelColor(strip.numPixels() - (i-(j*5)), color2)
            else:
                strip.setPixelColor(i-(j*5), color)
                strip.setPixelColor(strip.numPixels() - (i-(j*5)), color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorFullSlide(strip, color, color2, iterations=20, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(iterations):
        for j in range(-5, 5, 1):
            for k in range(0, strip.numPixels() + 5, 5):
                """r = strip.numPixels() - j"""
                if k%10 < 5:
                    strip.setPixelColor((k+j), color)
                else:
                    strip.setPixelColor((k+j), color2)
                time.sleep(wait_ms/140000.0)
            strip.show()

def colorFullSlideTransition(strip, color, color2, colorTrans, colorTrans2, invert=True, height=5, heightrans=5, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        if not invert: m = strip.numPixels() - i
        else: m = i
        for j in range(-5, 5, 1):
            jinv = -j
            for k in range(0, m, 5):
                if k+j <= m:
                    if k%10 < height:
                        strip.setPixelColor((k+j), colorTrans)
                    else:
                        strip.setPixelColor((k+j), colorTrans2)
                    time.sleep(wait_ms/300000.0)
            for l in range(m, strip.numPixels(), 5):
                if l+jinv >= m:
                    if (l - m)%10 < heightrans:
                        strip.setPixelColor((l+jinv), color)
                    else:
                        strip.setPixelColor((l+jinv), color2)
                    time.sleep(wait_ms/300000.0)
            strip.show()

def doubleColorFullSlide(strip, color, color2, iterations=20, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    numpixel = int(round(strip.numPixels()/2, 0))
    for i in range(iterations):
        for j in range(-5, 5, 1):
            for k in range(0, numpixel + 5, 5):
                if k%10 < 5:
                    strip.setPixelColor((k+j), color)
                    strip.setPixelColor(strip.numPixels() - (k+j), color)
                else:
                    strip.setPixelColor((k+j), color2)
                    strip.setPixelColor(strip.numPixels() - (k+j), color2)
                time.sleep(wait_ms/140000.0)
            strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def abiantic(strip, height=30, invert=False):
    for i in range (3):
        for j in range (0, height, 1):
            if invert: l = height - j
            else: l = j
            for k in range (0, strip.numPixels(), height):
                if i==0 : strip.setPixelColor(k + l, BLUE)
                elif i==1 <= 2 : strip.setPixelColor(k + l, RED)
                elif i==2 <= 3 : strip.setPixelColor(k + l, GREEN)
                strip.show()



def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
