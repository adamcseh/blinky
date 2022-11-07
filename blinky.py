#! /usr/bin/python3

from blinky_camera import *
#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


if __name__=="__main__":
    i = takeCalImage()
    plt.imshow(i)
    plt.savefig("cam/test_image.png")
    
