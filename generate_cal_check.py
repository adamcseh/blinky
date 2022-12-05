#! /usr/bin/python3

from blinky_cal import checkCalibration

if __name__=="__main__":
    filename = "cam/cal/front_cal.csv"
    checkCalibration(filename)