#! /usr/bin/python3
import numpy as np
import csv
from matplotlib import pyplot as plt

def loadCalData(filename:str):
    c = []
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            c.append((int(row[0]), float(row[1]), float(row[2])))
    return c

def plotCalibration(cal_data):
    led_index, x, y = zip(*cal_data)
    fig, ax = plt.subplots()
    ax.scatter(np.asarray(x),-1*np.asarray(y))
    for k in range(len(x)):
        ax.annotate(str(led_index[k]), (x[k], -1*y[k]))
    plt.show()

def hSegments(cal_data, x_size:int):
    led_index, x, y = zip(*cal_data)
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

def vSegments(cald_data, continuity:int=2):  # look for continuity in the led indexes
    led_index, x, y = zip(*cal_data)
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

def findLedsInSegment(h_seg, v_seg, x, y):
    h_led_indexes = h_seg[x]
    v_led_indexes = v_seg[y]
    led_indexes = []
    for led_index in h_led_indexes:
        if led_index in v_led_indexes:
            led_indexes.append(led_index) 
    return led_indexes

if __name__=="__main__":
    cal_data = loadCalData("cam\\cal\\front_cal.csv")
    hs = hSegments(cal_data, x_size=12)
    vs = vSegments(cal_data, continuity=10)
    print('horizontal segments:', hs)
    print('vertical segments:', vs)
    l = findLedsInSegment(hs, vs, 2, 0)
    print(l)
    plotCalibration(cal_data)