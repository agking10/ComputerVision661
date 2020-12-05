import numpy as np
from playsound import playsound
from pydub import AudioSegment
import time
from pydub.playback import play
import settings

THRESHOLD = 0.5

def playOneSound(sound, region):
    if (time.time() - settings.lastPlayed[region]) > THRESHOLD:
        settings.lastPlayed[region] = time.time()
        sound_path = "./sounds/"
        filename = sound_path + sound
        sound = AudioSegment.from_file(filename, format='wav')
        play(sound)


def playSound(coord, velocity, regions, references):

    threshold = 0

    row = coord[1]
    col = coord[0]

    region = regions[row][col]
    if region == 0:
        return
    target_vel = np.array(references[region][1])
    sound = references[region][0]
    speed = np.linalg.norm(velocity)
    cosine = np.dot(velocity, target_vel) / (speed * np.linalg.norm(target_vel))


    if cosine > 0.7 and speed > threshold:
        playOneSound(sound, region)


if __name__ == "__main__":
    playing = False
    regions = np.array([[1, 2], [3, 4]])
    references = {
        1: ('a.wav', [1, 1]),
        2: ('b.wav', [1, -1]),
        3: ('c.wav', [1, 1]),
        4: ('c2.wav', [1, 1])
    }

    velocity = np.array([1, 1])

    coords = []
    velocities = []

    playSound(coords, velocities, regions, references, playing)
    print("Played nothing")

    c1 = [0, 0]
    v1 = [1, 1]

    coords.append(c1)
    velocities.append(v1)

    playSound(coords, velocities, regions, references, playing)
    print("Played one sound")

    c2 = [0, 1]
    v2 = [1, -1]

    coords.append(c2)
    velocities.append(v2)

    playSound(coords, velocities, regions, references, playing)
    print("Played two sounds")

    c3 = [0, 1]
    v3 = [1, 1]

    coords = [c1, c3]
    velocities = [v1, v3]

    playSound(coords, velocities, regions, references, playing)
    print("Played one sound")

    c4 = [0, 0]
    v4 = [-1, 1]

    coords = [c3, c4]
    velocities = [v3, v4]

    playSound(coords, velocities, regions, references, playing)
    print("Played nothing again")

    playing = True
    coords = [c1, c2]
    velocities = [v1, v2]
    playSound(coords, velocities, regions, references, playing)
    print("Played nothing again")
