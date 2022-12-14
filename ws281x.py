#! /usr/bin/python3
import time
import numpy as np
from rpi_ws281x import PixelStrip, Color
from COLOR_CONSTANTS import *

# LED strip configuration:#1A1A1A#1A1A1A#1A1A1A#1A1A1A
LED_COUNT = 300      # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LEDstrip():
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
    def getPixels(self, first:int=0, last=None):
        n = self.strip.getPixels().size
        if not isinstance(last, int):
            last=n
        pixels = [-1 for k in range(0,n)]
        for k in range(first, last):
            pixels[k] = self.strip.getPixelColor(first+k)
        return pixels
    def setPixels(self, pixels:list):
        for p in pixels:
            self.strip.setPixelColor(p[0], p[1])
    def show(self):
        self.strip.show()
    def oneColorAll(self, color:int):
        n = self.strip.getPixels().size
        for k in range(0, n):
            self.strip.setPixelColor(k, color)
        self.strip.show()
        return color
    def blankAll(self):
        self.oneColorAll(BLANK_COLOR)
        return BLANK_COLOR
    def single(self, n:int, color=None):
        self.blankAll()
        if color:
            self.strip.setPixelColor(n, color)
        else:
            self.strip.setPixelColor(n, WHITE)
        self.strip.show()
    
# def colorPatch(strip:PixelStrip, offset:int, length:int, color:int, blank:bool=False):
#     if blank:
#         strip.blankAll()
#     for k in range(offset, offset+length):
#         strip.setPixelColor(k,color)
#     strip.show()
#     return color
    
# def noisy(strip:PixelStrip):
#     n = strip.getPixels().size
#     for p in range(0,n):
#         strip.setPixelColor(p, randomColor())
#     strip.show()
    
# def randomSnake(strip:PixelStrip, advance:int=1):
#     n = strip.getPixels().size
#     rotatePixels(strip, advance)
#     if advance>=0:
#         for p in range(0,advance%n):
#             strip.setPixelColor(p, randomColor())
#     else:
#         for p in range(n+advance,n):
#             strip.setPixelColor(p, randomColor())

# def rotatePixels(strip:PixelStrip, k:int):
#     pixels = getPixels(strip)
#     n = len(pixels)
#     for p in range(0,n):
#         strip.setPixelColor(p, pixels[(p-k)%n])
#     strip.show()
#     return k

if __name__ == '__main__':
    #strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    #strip.begin()
    #try:
    #    colorPatch(strip, offset=20, length=10, color=Color(0,0,255))
    #    while 1:
    #        #randomSnake(strip, advance=-1)
    #        noisy(strip)
    #        time.sleep(0.2)
    #except KeyboardInterrupt:
    #    blankAll(strip)
    #   print('goodbye')
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    for k in range(0,300):
        strip.setPixelColor(k,0)
    strip.show()
    print('done')
