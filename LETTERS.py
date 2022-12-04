from COLOR_CONSTANTS import *
import numpy as np

LETTERS = {
    "example":[[1,0,0,0,1],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [1,0,0,0,1]],
                 
    "example00":[[1,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]],
    
    "example11":[[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,1]],
                 
    "example10":[[0,0,0,0,1],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]],
                 
    "example01":[[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [1,0,0,0,0]],
                 
    "H": [[1,0,0,0,1],
          [1,0,0,0,1],
          [1,1,1,1,1],
          [1,0,0,0,1],
          [1,0,0,0,1]],

    "E": [[1,1,1,1,1],
          [1,0,0,0,1],
          [1,1,1,1,0],
          [1,0,0,0,0],
          [1,1,1,1,1]],

    "L": [[1,0,0,0,0],
          [1,0,0,0,0],
          [1,0,0,0,0],
          [1,0,0,0,0],
          [1,1,1,1,1]],
    
    "O": [[1,1,1,1,1],
          [1,0,0,0,1],
          [1,0,0,0,1],
          [1,0,0,0,1],
          [1,1,1,1,1]]
    }

def makeBlue(letter):
    return BLUE*np.asarray(letter)

#x for b in a for x in b
