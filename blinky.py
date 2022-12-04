#! /usr/bin/python3
from copy import deepcopy
import csv
import time
from blinky_camera import *
from ws281x import LEDstrip
import numpy as np
from PIL import Image
import pickle
from LETTERS import LETTERS, makeBlue
from fancy import SnowFall

def loadImage(filename:str):
    image = Image.open(filename).convert('RGB')
    i = np.asarray(image).astype(np.uint8)
    return np.asarray(image)

def saveImage(img_array, filename, verbose=False):
    if verbose:
        print('saveImage: ', np.shape(img_array))
    img = Image.fromarray(img_array.astype(np.uint8), "RGB")
    img.save(filename, "PNG")

def allBlackImage(rows, columns):
    return np.zeros((rows, columns, 3), dtype=np.uint8)
    
def monoColorImage(rows, columns, color_channel=0):
    img = allBlackImage(rows, columns)
    img[:][:][color_channel] = 255
    return img

def monoColor(img, color=0, verbose=False):
    if verbose:
        print('monoColor',np.shape(img))
    _img= deepcopy(img)
    _img[:][:][1] = img[:][:][1]
    return _img

def addCrossMark(image:np.array, x, y, size=1, verbose=False):
    # x-coordinate: columns
    # y-coordinate: rows
    rows = np.shape(image)[0]  
    columns = np.shape(image)[1]
    ncolors = np.shape(image)[2]
    if verbose:
        print('addCrossMark: ',x,y)
    _image = deepcopy(image)
    for k in range(0, ncolors):
        _image[y%rows][x%columns][k] = 255  # middle
        for j in range(0,size):
            _image[y%rows][(x-j)%columns][k] = 255  # left
        for j in range(0,size):  # right
            _image[y%rows][(x+j)%columns][k] = 255
        for j in range(0, size):
            _image[(y-j)%rows][x%columns][k] = 255  # top
        for j in range(0, size):
            _image[(y+j)%rows][x%columns][k] = 255  # bottom
    return _image

def findBrightestSpot(image:np.array, verbose=False):
    # x-coordinate: columns
    # y-coordinate: rows
    rows = np.shape(image)[0]
    columns = np.shape(image)[1]
    ncolors = np.shape(image)[2]
    flattened = np.zeros(rows*columns, dtype=np.uint)
    for k in range(0, ncolors):
        flattened += np.reshape(image[:,:,0], (1,rows*columns))[0]
    brightest = np.argmax(flattened)
    brightest_y = brightest//columns  # which column? -> integer division
    brightest_x = brightest%columns # which row? -> remainder
    if verbose:
        print("findBrightestSpot",columns, rows, ncolors,': ',brightest_x, brightest_y)
    return (brightest_x, brightest_y, np.sum(image[brightest_y][brightest_x][:]))
    
def manualCal(ledstrip, save=False):
    cal_data = []
    for k in range(0, 300):
        print("calibrating LED position:", k)
        ledstrip.single(k)
        img = takeCalImage()
        x,y,i = findBrightestSpot(img)
        print(x, y, i)
        print('wanna discard?')
        i = input() 
        if not i:
            cal_data.append((k,x,y))
            if save:
                img = addCrossMark(img, x,y,size=5)
                filename='cal_'+str(k)+'_x'+str(x)+'_y'+str(y)+'.png'
                saveImage(img, 'cam/cal/'+filename)
        print(cal_data)
    return cal_data
    
def loadNormalizedCalData(filename:str, verbose:bool=False):
    c = []
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            c.append((int(row[0]), float(row[1]), float(row[2])))
    return c
    
class matrixDisplay():
    def __init__(self, x_size:int, y_size:int, led_strip:LEDstrip, cal_data=None, verbose:bool=False):
        self.x_size = x_size
        self.y_size= y_size
        self.content = np.zeros((y_size, x_size), dtype=int)
        self.led_strip = led_strip
        self.points = cal_data  # list of (LED_number, x, y)
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

if __name__=="__main__":
    try:
        s = SnowFall(x_size=13, y_size=5, intensity=2)
        cal_data = loadNormalizedCalData('cam/cal_data.csv', verbose=False)
        ledstrip = LEDstrip()
        matrix = matrixDisplay(x_size=13,y_size=5,led_strip=ledstrip,cal_data=cal_data,verbose=False)
        c = makeBlue(LETTERS['O'])
        matrix._loadContent(c)
        leds = matrix._mapContent()
        matrix._displayContent(leds)
        
        #while 1:
        #    c = makeBlue(s.advance())
        #    matrix._loadContent(c, verbose=True)
        #    leds = matrix._mapContent(verbose=False)
        #    matrix._displayContent(leds)
        #    time.sleep(1)

    except KeyboardInterrupt:
        with open('cam/cal_data.pickle', 'wb') as pickle_file:
            pickle.dump(cal_data, pickle_file)
        ledstrip.blankAll()
    
