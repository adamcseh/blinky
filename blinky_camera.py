#! /usr/bin/python3
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

if __name__=="__main__":
    with picamera.PiCamera() as cam:
        cam.resolution = RESOLUTION
        cam.capture("./cam/picam_test_image.png")
