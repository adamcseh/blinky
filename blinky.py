#! /usr/bin/python3
import time
from ws281x import LEDstrip
import numpy as np
import pickle
from LETTERS import LETTERS, makeBlue
from fancy import SnowFall, MatrixDisplay     

if __name__=="__main__":
    try:
        ledstrip = LEDstrip()
        cal_file = 'cam/front_cal.csv'
        front_matrix = MatrixDisplay(x_size=13, y_size=5, led_strip=ledstrip, cal_file=cal_file, verbose=False)
        c = makeBlue(LETTERS['O'])
        front_matrix._loadContent(c)
        leds = front_matrix._mapContent()
        front_matrix._displayContent(leds)
        #s = SnowFall(x_size=13, y_size=5, intensity=2)
        #while 1:
        #    c = makeBlue(s.advance())
        #    matrix._loadContent(c, verbose=True)
        #    leds = matrix._mapContent(verbose=False)
        #    matrix._displayContent(leds)
        #    time.sleep(1)

    except KeyboardInterrupt:
        ledstrip.blankAll()
        print('this is the end')
