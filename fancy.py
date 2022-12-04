import numpy as np

class SnowFall():
    def __init__(self, x_size:int, y_size:int, intensity:int):
        self.x_size = x_size
        self.y_size = y_size
        self.intensity = intensity
        self.snapshot = np.zeros((y_size, x_size), dtype=int)
    def advance(self):
        for row in range(0, self.y_size-1):
            self.snapshot[self.y_size-row-1][:] = self.snapshot[self.y_size-row-2][:]
        self.snapshot[0][:] = np.zeros(self.x_size, dtype=int)
        for k in range(0, self.intensity):
            self.snapshot[0][np.random.randint(low=0,high=self.x_size)] = 1
        return self.snapshot
            
