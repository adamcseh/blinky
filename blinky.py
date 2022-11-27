#! /usr/bin/python3
from copy import deepcopy
from blinky_camera import *
from ws281x import LEDstrip
import numpy as np
from PIL import Image
import pickle

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
    
if __name__=="__main__":
    try:
        ledstrip = LEDstrip()
        cal_data = manualCal(ledstrip, save=True)
        with open('cam/cal_data.pickle', 'wb') as pickle_file:
            pickle.dump(cal_data, pickle_file)

    except KeyboardInterrupt:
        with open('cam/cal_data.pickle', 'wb') as pickle_file:
            pickle.dump(cal_data, pickle_file)
        ledstrip.blankAll()
    
