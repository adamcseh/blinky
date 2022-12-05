#! /usr/bin/python3
import numpy as np
from LETTERS import LETTERS

def generateBoard(text:str, y_size:int):
    b = np.zeros((y_size,1))
    for letter in text.replace(' ', '_').upper():
        b = np.hstack((b,LETTERS[letter]))
        b = np.hstack((b,LETTERS['single_separator']))
    return np.asarray(b)

if __name__=="__main__":
    board = generateBoard("hex" , 5)
    print(np.shape(board))
    print(board[:,1:])