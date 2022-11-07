import picamera
import numpy as np

RESOLUTION = (800, 608)
ARRAY_SIZE = list(RESOLUTION)
ARRAY_SIZE.reverse()
ARRAY_SIZE.append(3)

def takeCalImage():
    output = np.empty(ARRAY_SIZE, dtype=np.uint8)
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.capture(output, 'rgb')
    return output
