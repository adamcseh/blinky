#! /usr/bin/python3
import csv
import numpy as np
from PIL import Image
from blinky_camera import takeCalImage, findBrightestSpot, addCrossMark
from ws281x import LEDstrip

def manualCal(ledstrip:LEDstrip, save_images:bool=False, verbose:bool=False):
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
            if save_images:
                img = addCrossMark(img, x,y,size=5)
                filename='cal_'+str(k)+'_x'+str(x)+'_y'+str(y)+'.png'
                saveImage(img, 'cam/cal/'+filename)
        print(cal_data)
    normalized_cal_data = noramlizeCalData(cal_data, verbose=verbose)
    return normalized_cal_data

def saveImage(img_array, filename, verbose=False):
    if verbose:
        print('saveImage: ', np.shape(img_array))
    img = Image.fromarray(img_array.astype(np.uint8), "RGB")
    img.save(filename, "PNG")

def loadImage(filename:str):
    image = Image.open(filename).convert('RGB')
    i = np.asarray(image).astype(np.uint8)
    return np.asarray(image)

def noramlizeCalData(cal_data, verbose:bool=False):
    # find upper left (0,0) and lower right (1,1)
    x_min = cal_data[0][1]
    y_min = cal_data[0][2]
    x_max = cal_data[0][1]
    y_max = cal_data[0][2]
    for p in cal_data:
            if verbose:
                    print(p)
            if p[1] < x_min:
                    x_min = p[1]
            if p[2] < y_min:
                    y_min = p[2]
            if p[1] > x_max:
                    x_max = p[1]
            if p[2] > y_max:
                    y_max = p[2]
    if verbose:
            print("x_min: ", x_min)
            print("x_max: ", x_max)
            print("y_min: ", y_min)
            print("y_max: ", y_max)
    normalized = []
    for p in cal_data:
        n = (p[0], (p[1]-x_min)/(x_max-x_min), (p[2]-y_min)/(y_max-y_min))
        normalized.append(n)
        if verbose:
            print(n)
    return normalized

def saveCalData(cal_data, filename:str=None):
    if filename==None:
        filename = 'cam/cal_data.csv'
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        for p in cal_data:
            csv_writer.writerow(p)

def loadCalData(filename:str):
    c = []
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            c.append((int(row[0]), float(row[1]), float(row[2])))
    return c

if __name__ == "__main__":
    cal_file = 'cam/front_cal.csv'
    ledstrip = LEDstrip()
    normalized_cal_data = manualCal(ledstrip)
    saveCalData(normalized_cal_data, cal_file)
    c = loadCalData(cal_file)
    print(c)
