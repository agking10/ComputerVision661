import numpy as np
from playsound import playsound


def play(coords, velocity, regions, references):
    threshold = 0
    
    row = coords[0]
    col = coords[1]

    region = regions[row][col]
    if region==0:
        return
    target_vel = np.array(references[region][1])
    sound = references[region][0]
    speed = np.linalg.norm(velocity)
    cosine = np.dot(velocity, target_vel) / (speed * np.linalg.norm(target_vel))
    if cosine > 0.7 and speed > threshold:
        sound_path = "./sounds/"
        sound = sound_path + sound
        playsound(sound)


if __name__ == "__main__":
    regions = np.array([[1,2],[3,4]])
    references = {
        1: ('a.wav', [1,1]),
        2: ('b.wav', [1,1]),
        3: ('c.wav', [1,1]),
        4: ('c2.wav', [1,1])
    }

    velocity = np.array([1,1])

    x = 0
    y = 0
    for i in range(2):
        for j in range(2):
            play((x,y), velocity, regions, references)
            y += 1
        x += 1
        y = 0


                   
