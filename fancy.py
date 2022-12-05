import numpy as np
from ws281x import LEDstrip
from blinky_cal import loadCalData

class MatrixDisplay():
    def __init__(self, x_size:int, y_size:int, led_strip:LEDstrip, cal_file:str, verbose:bool=False):
        self.x_size = x_size
        self.y_size= y_size
        self.content = np.zeros((y_size, x_size), dtype=int)
        self.led_strip = led_strip
        self.points = loadCalData(cal_file) # list of (LED_number, x, y)
        if verbose:
            print(self.points)
    def _loadContent(self, new_content, verbose:bool=False):
        new_content_x_size = np.shape(new_content)[1]
        new_content_y_size = np.shape(new_content)[0]
        self.content = np.zeros((self.y_size, self.x_size), dtype=int)
        for x in range(0, min(self.x_size,new_content_x_size)):
            for y in range(0, min(self.y_size,new_content_y_size)):
                self.content[y][x] = new_content[y][x]
        if verbose:
            print(self.content)
    def _mapContent(self, verbose:bool=False):
        leds = []
        for _x in range(0, self.x_size):  # iterate over the ideal matrix display points
            for _y in range(0, self.y_size):  
                x = _x/(self.x_size-1)  # normalized x-coordiante (0,1)
                y = _y/(self.y_size-1)  # normalized y-coordiante (0,1)
                d2 = []
                for p in self.points:
                    d2.append(np.abs((p[1]-x)**2+(p[2]-y)**2))  # distance from actual points
                led_index = self.points[np.argmin(d2)][0]
                led_index_already_registered = False
                for l in leds:
                    if l[0] == led_index:
                        led_index_already_registered = True
                        break
                if not led_index_already_registered:
                    leds.append((led_index,int(self.content[_y][_x])))
        return leds
    def _displayContent(self, leds):
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
            
