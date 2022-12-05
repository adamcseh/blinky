#! /usr/bin/python3
import time
from ws281x import LEDstrip
import numpy as np
from LETTERS import LETTERS, makeColor
from COLOR_CONSTANTS import *
from fancy import SnowFall, MatrixDisplay     

def generateBoard(text:str, y_size:int):
    b = np.zeros((y_size,1))
    for letter in text.replace(' ', '_').upper():
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
        front_matrix = MatrixDisplay(x_size=x_size, y_size=y_size, led_strip=ledstrip, cal_file=cal_file, verbose=False)
        msg = "hello silabs"
        board, length = generateBoard(msg, y_size)
        print(np.shape(board))
        iteration = 0
        while 1:
            c = getBoardSubset(board, iteration, x_size)
            c = makeColor(c, WHITE)
            front_matrix._loadContent(c)
            leds = front_matrix._mapContent()
            front_matrix._displayContent(leds)
            iteration+=1
            time.sleep(0.3)
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
