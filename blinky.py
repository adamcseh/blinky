#! /usr/bin/python3
import time
from ws281x import LEDstrip
import numpy as np
from LETTERS import LETTERS, makeColor
from COLOR_CONSTANTS import *
from fancy import SnowFall, MatrixDisplay, RainbowSweep     

def generateBoard(text:str, y_size:int):
    b = np.zeros((y_size,1))
    t = text.upper().replace(' ', '_')
    for letter in t:
        b = np.hstack((b,LETTERS[letter]))
        b = np.hstack((b,LETTERS['single_separator']))
    length = np.shape(b)[1]
    return b, length

def getBoardSubset(board, offset, length):
    board_length = np.shape(board)[1]
    start = offset%board_length
    stop = (start+length)%board_length
    if stop>start:
        subset = board[:,start:stop]
    else:
        subset = np.hstack((board[:,start:-1],board[:,0:stop]))
    return subset

if __name__=="__main__":
    try:
        ledstrip = LEDstrip()
        cal_file = 'cam/cal/front_cal.csv'
        x_size = 11
        y_size = 5
        front_matrix = MatrixDisplay(x_size=x_size, y_size=y_size, led_strip=ledstrip, cal_file=cal_file)
        snowing = SnowFall(x_size=x_size, y_size=y_size, intensity=2)
        rainbow = RainbowSweep()
        mode = '3'
        msg = "merry xmas silabs "
        while 1:
            try:
                if mode=='1':
                    board, length = generateBoard(msg, y_size)
                    iteration = 0
                    print("starting scrolling text")
                    while 1:
                        c = getBoardSubset(board, iteration, x_size)
                        c = makeColor(c, WHITE)
                        front_matrix.loadContent(c)
                        leds = front_matrix.mapContent2()
                        front_matrix.displayContent(leds)
                        iteration+=1
                        time.sleep(0.07)
                elif mode=='2':
                    print("starting snowfall")
                    while 1:
                        s = snowing.advance()
                        s = makeColor(s, WHITE)
                        front_matrix.loadContent(s)
                        leds = front_matrix.mapContent2()
                        front_matrix.displayContent(leds)
                        time.sleep(0.3)
                elif mode=="3":
                    print("startin lgbtq")
                    while 1:
                        r = rainbow.advance()
                        front_matrix.displayContent(r)
                else:
                    print("unknown mode")
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                print("select mode")
                print("1: scrolling text; 2: snowfall; 3: color sweep")
                m = input()
                if m=='1':
                    print("text to display: ")
                    msg = input()
                mode = m
    except KeyboardInterrupt:
        ledstrip.blankAll()
        print('this is the end')
                
                

        #s = SnowFall(x_size=13, y_size=5, intensity=2)
        #while 1:
        #    c = makeBlue(s.advance())
        #    matrix._loadContent(c, verbose=True)
        #    leds = matrix._mapContent(verbose=False)
        #    matrix._displayContent(leds)
        #    time.sleep(1)

    
