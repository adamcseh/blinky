import numpy as np
from ws281x import LEDstrip
from blinky_cal import loadCalData
from COLOR_CONSTANTS import *

class MatrixDisplay():
    def __init__(self, x_size:int, y_size:int, led_strip:LEDstrip, cal_file:str):
        self.x_size = x_size
        self.y_size= y_size
        self.content = np.zeros((y_size, x_size), dtype=int)
        self.led_strip = led_strip
        self.cal_data = loadCalData(cal_file) # list of (LED_number, x, y)
        self.hSegments = self._hSegments(self.x_size)
        self.vSegments = self._vSegments(continuity=10)
    def _hSegments(self, x_size:int):
        led_index, x, y = zip(*self.cal_data)
        x = np.asarray(x)
        y = np.asarray(y)
        led_index = np.asarray(led_index)
        dx= np.abs(np.max(x)-np.min(x))
        cell_width = dx*(1+1/x_size)/x_size
        x0 = np.min(x)-cell_width/2
        leds_by_segment = []
        for s in range(0, x_size):  # iterate over the segments and group leds
            leds_in_this_segment = []
            for l in range(0, len(led_index)):
                if x[l]>x0+s*cell_width and x[l]<x0+(s+1)*cell_width:
                    leds_in_this_segment.append(led_index[l])
            leds_by_segment.append(leds_in_this_segment)
        return leds_by_segment
    def _vSegments(self, continuity:int=2):  # look for continuity in the led indexes
        led_index, x, y = zip(*self.cal_data)
        x = np.asarray(x)
        y = np.asarray(y)
        led_index = np.asarray(led_index)
        last_led_index = led_index[0]
        leds_by_segment=[]
        leds_in_this_segment = []
        for k in range(0, len(led_index)):
            if np.abs(led_index[k]-last_led_index) < continuity:
                leds_in_this_segment.append(led_index[k])
            else:  # reached the end of a segment
                leds_by_segment.append(leds_in_this_segment)  # save the segment
                leds_in_this_segment = []  # reset the storing array
                leds_in_this_segment.append(led_index[k])  # store the first element
            last_led_index = led_index[k]
        leds_by_segment.append(leds_in_this_segment)
        leds_by_segment.reverse()
        return leds_by_segment
    def _findLedsInSegment(self, x, y):
        h_led_indexes = self.hSegments[x]
        v_led_indexes = self.vSegments[y]
        led_indexes = []
        for led_index in h_led_indexes:
            if led_index in v_led_indexes:
                led_indexes.append(led_index) 
        return led_indexes
    def loadContent(self, new_content, verbose:bool=False):
        new_content_x_size = np.shape(new_content)[1]
        new_content_y_size = np.shape(new_content)[0]
        self.content = np.zeros((self.y_size, self.x_size), dtype=int)
        for x in range(0, min(self.x_size,new_content_x_size)):
            for y in range(0, min(self.y_size,new_content_y_size)):
                self.content[y][x] = new_content[y][x]
        if verbose:
            print(self.content)
    def mapContent(self):
        leds = []
        for _x in range(0, self.x_size):  # iterate over the ideal matrix display points
            for _y in range(0, self.y_size):  
                x = _x/(self.x_size-1)  # normalized x-coordiante (0,1)
                y = _y/(self.y_size-1)  # normalized y-coordiante (0,1)
                d2 = []
                for p in self.cal_data:
                    d2.append(np.abs((p[1]-x)**2+(p[2]-y)**2))  # distance from actual points
                led_index = self.cal_data[np.argmin(d2)][0]
                led_index_already_registered = False
                for l in leds:
                    if l[0] == led_index:
                        led_index_already_registered = True
                        break
                if not led_index_already_registered:
                    leds.append((int(led_index),int(self.content[_y][_x])))
        return leds
    def mapContent2(self):
        leds = []
        for _x in range(self.x_size):
            for _y in range(self.y_size):
                if self.content[_y][_x] != 0:
                    leds_to_lit = self._findLedsInSegment(_x, _y)
                    leds.append([(int(l), int(self.content[_y][_x])) for l in leds_to_lit])
        return [item for sublist in leds for item in sublist]

    def displayContent(self, leds):
        self.led_strip.blankAll()
        self.led_strip.setPixels(leds)
        self.led_strip.show()       

class SnowFall():
    def __init__(self, x_size:int, y_size:int, intensity:int):
        self.x_size = x_size
        self.y_size = y_size
        self.intensity = intensity
        self.snapshot = np.zeros((y_size, x_size), dtype=int)
    def advance(self):
        for row in range(0, self.y_size-1):
            self.snapshot[self.y_size-row-1][:] = self.snapshot[self.y_size-row-2][:]
        self.snapshot[0][:] = np.zeros(self.x_size, dtype=int)
        for k in range(0, self.intensity):
            self.snapshot[0][np.random.randint(low=0,high=self.x_size)] = 1
        return self.snapshot
            
