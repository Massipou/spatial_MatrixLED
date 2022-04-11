from MATRIX import *

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            #rainbow(strip)
            #sound_react_mov_mirror_div2(strip, 80, False, 2, 100, 50)
            sound_react_mov(strip, 2, True, 2)
            sound_react_mov(strip, 2, False, 2)

            #sound_react_mov_mirror(strip, 2, True, 2)


            # sound_react_mov(strip, 20, True, 2)
            # sound_react_div(strip, 10, 10, 2)
            # sound_react_div(strip, 20, 5, 2)
            # sound_react_div_mov(strip, 10, 20, 2)
            # sound_react_div_mov(strip, 20, 5, 2)
            # sound_react_mov(strip, 20, True, 2)


            print ("BONNE NUIT LES PETITS ! 8=D \(!)/")

            # abiantic(strip)
            # abiantic(strip, 30, True)
            # abiantic(strip, 20)
            # abiantic(strip, 20, True)
            # abiantic(strip, 10)
            # abiantic(strip, 10, True)
            # colorFullSlideTransition(strip, BLUE, GREEN, GREEN, RED, False, 1)
            # colorFullSlideTransition(strip, MAGICRED, BLUEPURP, GREEN, RED)
            # doubleColorSlide(strip, BLUEPURP, GREEN)
            # doubleColorFullSlide(strip, BLUEPURP, GREEN)
            # doubleColorSlide(strip, GREEN, RED)
            # doubleColorFullSlide(strip, GREEN, RED)
            # doubleColorSlide(strip, DARKVIOLET, MAGICRED)
            # doubleColorFullSlide(strip, DARKVIOLET, MAGICRED)

            # print ('Theater chase animations.')
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        for i in range (strip.numPixels()):
            strip.setPixelColor(i, DOWN)
        strip.show()
