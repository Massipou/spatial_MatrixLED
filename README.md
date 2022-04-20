# SPATIAL MATRIX LED
 
## This project is an Web interface for control WS2812 with audio input.

## needed: 
- rasberry pi
- WS2812 stripes
- pc with microphone

## Concept:
Use your laptop for listen default audio input (like microphone) and generate interactive RBG color with it.
The laptop is also a web server with interactive audio EQ, color modulator, effects and template inputs.

The raspberry pi is a generator of animations for WS2812 LED strpes.
He listen to the color emited by the laptop via network connexion for create stripe led animations.

## Install ...
pi_spaceled folder need to be intalled on a raspberry pi.
webserver_spaceled folder need to be intalled on a laptop who is network connected to the pi.

pattern.py have to be run on the a raspberry with python3
after that run flask app "webled.py" on the pc.

## What eles ???

Tryed with a Debian 10 laptop, a Raspberry pi 4 and a stripes of 600 WS2812 led.
