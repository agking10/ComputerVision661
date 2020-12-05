import time
import numpy as np

def init(regions):
    global lastPlayed
    lastPlayed = {}
    for n in regions:
        lastPlayed[n] = time.time()
    lastPlayed[0] = np.inf