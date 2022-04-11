#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy
import math

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

