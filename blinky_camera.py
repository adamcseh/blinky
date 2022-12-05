#! /usr/bin/python3
from copy import deepcopy
import picamera
import numpy as np

RESOLUTION = (800, 608)
ARRAY_SIZE = list(RESOLUTION)
ARRAY_SIZE.reverse()
ARRAY_SIZE.append(3)

def takeCalImage(bw=False):
    img = np.empty(ARRAY_SIZE, dtype=np.uint8)
    with picamera.PiCamera() as camera:
        if bw:
            camera.color_effects = (128,128)  # black and white mode
        camera.resolution = RESOLUTION
        camera.capture(img, format='rgb')
    return img

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

if __name__=="__main__":
    with picamera.PiCamera() as cam:
        cam.resolution = RESOLUTION
        cam.capture("./cam/picam_test_image.png")
