#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy
import math
import socket
import threading

RATE = 44100
BUFFER = 882

p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.5.1', 8088))

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def get_sound_data():
    try:
        data = numpy.fft.rfft(numpy.fromstring(
            stream.read(BUFFER), dtype=numpy.float32)
        )
    except IOError:
        pass
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
    return (data)

def freqindex(freq):
    return round(int(freq /50))

def data_sender(r="0", g="0", b="0", data="0", zoom="0"):
    data_to_send = "{} {} {} {} {}" .format(r, g, b, data, zoom)
    #print("{} {} {} {} {}" .format(r, g, b, data, zoom))
    s.send(data_to_send.encode())

def freq_to_color2(rseuil = 15, gseuil = 14, bseuil = 15, red = 0, green = 255, blue = 0):
    sounddata = get_sound_data()
    bassmax = -60
    midmax = -60
    highmax = -60


    for i in range (50, 200, 50):
        if sounddata[freqindex(i)] > bassmax : bassmax = sounddata[freqindex(i)]
    for i in range (250, 500, 50):
        if sounddata[freqindex(i)] > midmax : midmax = sounddata[freqindex(i)]
    for i in range (500, 2000, 50):
        if sounddata[freqindex(i)] > highmax : highmax = sounddata[freqindex(i)]

    if -bassmax < rseuil or -midmax < gseuil or -highmax < bseuil:
        r = int(red)
        g = int(green)
        b = int(blue)
    else: r, g, b = 0, 0, 0

    #if -midmax < gseuil:
    #    g = int(round(((midmax + gseuil)/3)**4))
    #    if g < 0: g = 0
    #    if g > 255: g = 255
    #else: g = 0
    #if -highmax < bseuil:
    #    b = int(round(((highmax + bseuil)/4)**4))
    #    if b < 0: b = 0
    #    if b > 255: b = 255
    #else: b = 0
    #print ("{}, {}" .format(highmax, bseuil))

    return (r, g, b)

class threadColorSender (threading.Thread):
   def __init__(self, threadID, name, R, G, B):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.r = R
      self.g = G
      self.b = B
      self.data = ""
      self.zoom = ""
      self.red = "0"
      self.green = "255"
      self.blue = "0"
   def run(self):
        while True:
            r, g, b = freq_to_color2(self.r, self.g, self.b, self.red, self.green, self.blue)
            data_sender(r, g, b, self.data, self.zoom)
            #print("{} {}".format(self.data, self.zoom))
            self.data = "0"
            self.zoom = "0"
