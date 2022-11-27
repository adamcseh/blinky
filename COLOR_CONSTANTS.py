import numpy as np
from rpi_ws281x import Color

BLANK_COLOR = 0
BLUE = 255
WHITE = 2**24-1

def randomColor():
    r = np.random.randint(255)
    g = np.random.randint(255)
    b = np.random.randint(255)
    return Color(r,g,b)
